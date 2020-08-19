# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
#

import math

import torch
import torch.nn.functional as F
from fairseq import utils
from . import FairseqCriterion, register_criterion


@register_criterion("word_knowledge_distillation")
class KnowledgeDistillationCriterion(FairseqCriterion):
    def __init__(self, args, task):
        super().__init__(args, task)
        assert (
            args.teacher_path
        ), "Please specify at least one valid file for --teacher-path"
        use_cuda = torch.cuda.is_available() and not self.args.cpu

        # Load model ensemble from checkpoints
        self.teacher_models, self.teacher_model_args = utils.load_ensemble_for_inference(
            args.teacher_path.split(":"), task
        )

        # Move models to device and to evaluation mode
        if use_cuda:
            for model in self.teacher_models:
                if args.fp16:
                    model = model.half()
                model.cuda()

        self.kd_weight = getattr(args, "kd_weight", 1)
        if self.kd_weight < 0 or self.kd_weight > 1:
            raise ValueError(f"--kd-weight ({self.kd_weight}) must be in [0, 1]")

    @staticmethod
    def add_args(parser):
        """Add criterion-specific arguments to the parser."""
        parser.add_argument(
            "--teacher-path",
            metavar="FILE",
            help="path(s) to teacher model file(s) colon separated",
        )
        parser.add_argument(
            "--kd-weight",
            type=float,
            default=0.0,
            help=(
                "mixture weight between the knowledge distillation and",
                "negative log likelihood losses. Must be in [0.0, 1.0]",
            ),
        )

    def forward(self, model, sample, reduce=True):
        """Compute the loss for the given sample.
        Returns a tuple with three elements:
        1) the loss, as a Variable
        2) the sample size, which is used as the denominator for the gradient
        3) logging outputs to display while training
        """
        masked_tokens = sample['target'].ne(self.padding_idx)
        sample_size = masked_tokens.int().sum().item()

        if sample_size == 0:
            masked_tokens = None

        # 1. Generate translation using student model
        net_output = model(**sample["net_input"], masked_tokens=masked_tokens)
        lprobs = model.get_normalized_probs(net_output, log_probs=True)

        # [bsz, seqlen, vocab] -> [bsz*seqlen, vocab]
        lprobs = lprobs.view(-1, lprobs.size(-1))

        # 2. Generate translation using teacher models
        avg_probs = None
        with torch.no_grad():
            for teacher_model in self.teacher_models:
                teacher_output = teacher_model(**sample["net_input"], masked_tokens=masked_tokens)
                probs = teacher_model.get_normalized_probs(teacher_output, log_probs=False)
                if avg_probs is None:
                    avg_probs = probs
                else:
                    avg_probs.add_(probs)

        avg_probs.div_(len(self.teacher_models))
        avg_probs = avg_probs.view(-1, avg_probs.size(-1)).detach()
        kd_loss = -torch.sum(avg_probs * lprobs)

        # 3. Compute NLL loss with respect to the ground truth
        target = model.get_targets(sample, net_output)[masked_tokens].view(-1)
        nll_loss = F.nll_loss(
            lprobs,
            target,
            size_average=False,
            ignore_index=self.padding_idx,
            reduce=reduce,
        )

        # 4. Linearly interpolate between NLL and KD loss
        if model.training is True:
            loss = kd_loss * self.kd_weight + nll_loss * (1 - self.kd_weight)
        else:
            loss = nll_loss

        logging_output = {
            "loss": utils.item(loss.data) if reduce else loss.data,
            'nll_loss': utils.item(loss.data) if reduce else loss.data,
            "ntokens": sample["ntokens"],
            "nsamples": sample["target"].size(0),
            "sample_size": sample_size,
        }
        return loss, sample_size, logging_output

    @staticmethod
    def aggregate_logging_outputs(logging_outputs):
        """Aggregate logging outputs from data parallel training."""
        loss_sum = sum(log.get("loss", 0) for log in logging_outputs)
        ntokens = sum(log.get("ntokens", 0) for log in logging_outputs)
        nsentences = sum(log.get("nsentences", 0) for log in logging_outputs)
        sample_size = sum(log.get("sample_size", 0) for log in logging_outputs)
        agg_output = {
            "loss": loss_sum / sample_size / math.log(2),
            'nll_loss': sum(log.get('nll_loss', 0) for log in logging_outputs) / sample_size / math.log(2) if ntokens > 0 else 0.,
            "ntokens": ntokens,
            "nsentences": nsentences,
            "sample_size": sample_size,
        }
        return agg_output
