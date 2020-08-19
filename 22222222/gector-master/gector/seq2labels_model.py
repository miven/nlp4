"""Basic model. Predicts tags for every token"""
from typing import Dict, Optional, List, Any

import numpy
import torch
import torch.nn.functional as F
from allennlp.data import Vocabulary
from allennlp.models.model import Model
from allennlp.modules import TimeDistributed, TextFieldEmbedder
from allennlp.nn import InitializerApplicator, RegularizerApplicator
from allennlp.nn.util import get_text_field_mask, sequence_cross_entropy_with_logits
from allennlp.training.metrics import CategoricalAccuracy
from overrides import overrides
from torch.nn.modules.linear import Linear


@Model.register("seq2labels")
class Seq2Labels(Model):
    """
    This ``Seq2Labels`` simply encodes a sequence of text with a stacked ``Seq2SeqEncoder``, then
    predicts a tag (or couple tags) for each token in the sequence.

    Parameters
    ----------
    vocab : ``Vocabulary``, required
        A Vocabulary, required in order to compute sizes for input/output projections.
    text_field_embedder : ``TextFieldEmbedder``, required
        Used to embed the ``tokens`` ``TextField`` we get as input to the model.
    encoder : ``Seq2SeqEncoder``
        The encoder (with its own internal stacking) that we will use in between embedding tokens
        and predicting output tags.
    calculate_span_f1 : ``bool``, optional (default=``None``)
        Calculate span-level F1 metrics during training. If this is ``True``, then
        ``label_encoding`` is required. If ``None`` and
        label_encoding is specified, this is set to ``True``.
        If ``None`` and label_encoding is not specified, it defaults
        to ``False``.
    label_encoding : ``str``, optional (default=``None``)
        Label encoding to use when calculating span f1.
        Valid options are "BIO", "BIOUL", "IOB1", "BMES".
        Required if ``calculate_span_f1`` is true.
    label_namespace : ``str``, optional (default=``labels``)
        This is needed to compute the SpanBasedF1Measure metric, if desired.
        Unless you did something unusual, the default value should be what you want.
    verbose_metrics : ``bool``, optional (default = False)
        If true, metrics will be returned per label class in addition
        to the overall statistics.
    initializer : ``InitializerApplicator``, optional (default=``InitializerApplicator()``)
        Used to initialize the model parameters.
    regularizer : ``RegularizerApplicator``, optional (default=``None``)
        If provided, will be used to calculate the regularization penalty during training.
    """

    def __init__(self, vocab: Vocabulary,
                 text_field_embedder: TextFieldEmbedder,
                 predictor_dropout=0.0,
                 labels_namespace: str = "labels",
                 detect_namespace: str = "d_tags",
                 verbose_metrics: bool = False,
                 label_smoothing: float = 0.0,
                 confidence: float = 0.0,
                 initializer: InitializerApplicator = InitializerApplicator(),
                 regularizer: Optional[RegularizerApplicator] = None) -> None:
        super(Seq2Labels, self).__init__(vocab, regularizer)

        self.label_namespaces = [labels_namespace,
                                 detect_namespace]
        self.text_field_embedder = text_field_embedder
        self.num_labels_classes = self.vocab.get_vocab_size(labels_namespace) # 使用最新的分类数量.
        self.num_detect_classes = self.vocab.get_vocab_size(detect_namespace)
        self.label_smoothing = label_smoothing
        self.confidence = confidence
        self.incorr_index = self.vocab.get_token_index("INCORRECT",
                                                       namespace=detect_namespace)

        self._verbose_metrics = verbose_metrics
        self.predictor_dropout = TimeDistributed(torch.nn.Dropout(predictor_dropout))

        self.tag_labels_projection_layer = TimeDistributed(
            Linear(text_field_embedder._token_embedders['bert'].get_output_dim(), self.num_labels_classes)) # 把768映射到28  ,可以修改Linear为transformer # 这个地方只是一个全连接,可以改成更复杂的网络.

        self.tag_detect_projection_layer = TimeDistributed(
            Linear(text_field_embedder._token_embedders['bert'].get_output_dim(), self.num_detect_classes)) # 把768映射到4

        self.metrics = {"accuracy": CategoricalAccuracy()}

        initializer(self)

    @overrides
    def forward(self,  # type: ignore
                tokens: Dict[str, torch.LongTensor],
                labels: torch.LongTensor = None,
                d_tags: torch.LongTensor = None,
                metadata: List[Dict[str, Any]] = None) -> Dict[str, torch.Tensor]:
        # pylint: disable=arguments-differ
        """
        Parameters
        ----------
        tokens : Dict[str, torch.LongTensor], required
            The output of ``TextField.as_array()``, which should typically be passed directly to a
            ``TextFieldEmbedder``. This output is a dictionary mapping keys to ``TokenIndexer``
            tensors.  At its most basic, using a ``SingleIdTokenIndexer`` this is: ``{"tokens":
            Tensor(batch_size, num_tokens)}``. This dictionary will have the same keys as were used
            for the ``TokenIndexers`` when you created the ``TextField`` representing your
            sequence.  The dictionary is designed to be passed directly to a ``TextFieldEmbedder``,
            which knows how to combine different word representations into a single vector per
            token in your input.
        lables : torch.LongTensor, optional (default = None)
            A torch tensor representing the sequence of integer gold class labels of shape
            ``(batch_size, num_tokens)``.
        d_tags : torch.LongTensor, optional (default = None)
            A torch tensor representing the sequence of integer gold class labels of shape
            ``(batch_size, num_tokens)``.
        metadata : ``List[Dict[str, Any]]``, optional, (default = None)
            metadata containing the original words in the sentence to be tagged under a 'words' key.

        Returns
        -------
        An output dictionary consisting of:
        logits : torch.FloatTensor
            A tensor of shape ``(batch_size, num_tokens, tag_vocab_size)`` representing
            unnormalised log probabilities of the tag classes.
        class_probabilities : torch.FloatTensor
            A tensor of shape ``(batch_size, num_tokens, tag_vocab_size)`` representing
            a distribution of the tag classes per word.
        loss : torch.FloatTensor, optional
            A scalar loss to be optimised.

        """  # 下面就是整个翻译模型的算法架构.
        '''
        手动shuffle, 外卖的shuffle不好使,不知道为什么!!!!!!!!!!!!!!!!
        '''
        if metadata:
            import random

            chang = len(metadata)
            tmp = list(range((chang)))
            random.shuffle(tmp)
            print('\n')
            print('                      ')
            print('                      ')
            print('                      ')
            print('                      ')
            print('                      ')
            print('                      ')
            print('                      ')
            print('                      ')
            print('                      ')
            print(tmp, '修改后的顺序是')
            # tokens['bert'].numpy()[1,2,3,4,0]    tokens['bert'][[2,3,4,0,1],:]
            tokens['bert']= tokens['bert'][tmp,:]
            tokens['bert-offsets']= tokens['bert-offsets'][tmp,:]
            tokens['mask']= tokens['mask'][tmp,:]
            labels= labels[tmp,:]
            d_tags= d_tags[tmp,:]
            import numpy as np
            metadata=np.array(metadata)
            metadata= metadata[tmp]
# shuffle 完毕.












        encoded_text = self.text_field_embedder(tokens)  # 第一步先用pre_trained embedding
        batch_size, sequence_length, _ = encoded_text.size()  # 整个算法的输入.(9, 50, 768) 每一个单词看做一个token.
        mask = get_text_field_mask(tokens)  # 就是把补全到50的padding 标志位0,其他标志位1.   torch.Size([9, 50])
        logits_labels = self.tag_labels_projection_layer(   self.predictor_dropout(encoded_text)   )  #torch.Size([9, 50, 28])# 28分类问题
        logits_d = self.tag_detect_projection_layer(encoded_text) # 4分类问题  #torch.Size([9, 50, 4])

        class_probabilities_labels = F.softmax(logits_labels, dim=-1).view( #!!!!!!!!!!!!!!!!!!!!!!!!!---------------------
            [batch_size, sequence_length, self.num_labels_classes]) #----------------class_probabilities_labels 这个是核心的输出,只用这个就可以得到最后output
        import numpy as np

        # ???????????????这行为什么报错????????np.array(class_probabilities_labels)    #----------------class_probabilities_labels 这个是核心的输出,只用这个就可以得到最后output
        # from predict import confidence
        # #  下面做 置信度finetune, 把置信度 <args.   ----------------
        # tmp=confidence

        # with open('conf', ) as f:
        #     tmp = float(f.readlines()[0])
        # if tmp!=0:
        #     tmp2=(class_probabilities_labels.numpy()[:,:,1:]>tmp).astype(int)
        #     class_probabilities_labels[:,:,1:]=torch.tensor(tmp2)













        class_probabilities_d = F.softmax(logits_d, dim=-1).view(
            [batch_size, sequence_length, self.num_detect_classes])
        error_probs = class_probabilities_d[:, :, self.incorr_index] * mask # 那些padding的loss不需要计算,没意义.
        incorr_prob = torch.max(error_probs, dim=-1)[0]  # 按照一句话里面错率最大的字来算整个句子的错误率.

        if self.confidence > 0:
            probability_change = [self.confidence] + [0] * (self.num_labels_classes - 1)
            class_probabilities_labels += torch.FloatTensor(probability_change).repeat(
                (batch_size, sequence_length, 1))

        output_dict = {"logits_labels": logits_labels,
                       "logits_d_tags": logits_d,
                       "class_probabilities_labels": class_probabilities_labels,
                       "class_probabilities_d_tags": class_probabilities_d,
                       "max_error_probability": incorr_prob}
        # 下面只在训练的时候输出,因为只有训练的时候才有labels这个 groud_true标签. predict时候会跳过下面代码.!!!!!!!!!!!!!!!!!!!!!!!!!!!1        2020-07-08,18点49
        if labels is not None and d_tags is not None: # sequence_cross_entropy_with_logits 这个里面yhat 不用softmax? 这个点进去看说明就可以,他里面说了不用归一化之后的数据,直接输入即可. 诡异话之后的数据是class_probabilities_labels
            loss_labels = sequence_cross_entropy_with_logits(logits_labels, labels, mask,
                                                             label_smoothing=self.label_smoothing) # logits_labels 是28分类的概率分布, labels是 y标签. mask是遮罩也就是带入的weights. 用这个来算交叉熵.
            from train_finetune_latest2 import vocabdir
            with open(vocabdir) as f:
                tmp3=f.readlines()
            tmp3=[i.strip('\n') for i in tmp3]
            tmp3=np.array(tmp3)




            loss_d = sequence_cross_entropy_with_logits(logits_d, d_tags, mask) # 同理
            for metric in self.metrics.values():
                metric(logits_labels, labels, mask.float())
                metric(logits_d, d_tags, mask.float())
            output_dict["loss"] = loss_labels + loss_d
            print('\n ------------------------------------------------\n')
            print('\n ------------------------------------------------\n')
            print('\n ------------------------------------------------\n')
            print('\n ------------------------------------------------\n')
            print('我们打印几个看看,目前策略是只打印最后2个,为了保证算法不会过多损耗性能.看看预测的结果是否是我们打的tag:')
            print('我们打印,最大分类标签和置信度.')
            allfenlei=torch.max(class_probabilities_labels, dim=-1)[1][-2:]# 这个东西我们用来生成标签.这个是所有的分类标签.
            gailv=torch.max(class_probabilities_labels, dim=-1)[0][-2:]# 这个东西我们用来生成标签.这个是所有的分类标签.
            newlist=[]
            for ii2 in range(len(allfenlei)):
                saveindex=[i for i in range(len(allfenlei[ii2])) if allfenlei[ii2][i]!=0]
                newlist.append(gailv[ii2][saveindex])
            shuju=metadata[-2:]
            for jj in range(len(allfenlei)):
                print('原始句子为',shuju[jj])
                tmp=[i for i in allfenlei[jj] if i!=0]
                print('输出的变换为','\t'.join(tmp3[tmp]))
                print('对应的概率为')
                print(newlist[jj])
            print('------------该epoch评测完毕.')
            # 原始数据是metadata.所以也打印一下,对比一下效果.
















        if metadata is not None:
            output_dict["words"] = [x["words"] for x in metadata]
        return output_dict

    @overrides
    def decode(self, output_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Does a simple position-wise argmax over each token, converts indices to string labels, and
        adds a ``"tags"`` key to the dictionary with the result.
        """
        for label_namespace in self.label_namespaces:
            all_predictions = output_dict[f'class_probabilities_{label_namespace}']
            all_predictions = all_predictions.cpu().data.numpy()
            if all_predictions.ndim == 3:
                predictions_list = [all_predictions[i] for i in range(all_predictions.shape[0])]
            else:
                predictions_list = [all_predictions]
            all_tags = []

            for predictions in predictions_list:
                argmax_indices = numpy.argmax(predictions, axis=-1)
                tags = [self.vocab.get_token_from_index(x, namespace=label_namespace)
                        for x in argmax_indices]
                all_tags.append(tags)
            output_dict[f'{label_namespace}'] = all_tags
        return output_dict

    @overrides
    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        metrics_to_return = {metric_name: metric.get_metric(reset) for
                             metric_name, metric in self.metrics.items()}
        return metrics_to_return
