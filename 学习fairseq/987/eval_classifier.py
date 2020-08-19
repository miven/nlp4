from fairseq import checkpoint_utils, data, options, tasks

# Parse command-line arguments for generation
parser = options.get_generation_parser(default_task='simple_classification')
args = options.parse_args_and_arch(parser)

# Setup task
task = tasks.setup_task(args)

# Load model
print('| loading model from {}'.format(args.path))
models, _model_args = checkpoint_utils.load_model_ensemble([args.path], task=task)
model = models[0]

while True:
    sentence = input('\nInput: ')

    # Tokenize into characters
    chars = ' '.join(list(sentence.strip()))
    tokens = task.source_dictionary.encode_line(
        chars, add_if_not_exist=False,
    )

    # Build mini-batch to feed to the model
    batch = data.language_pair_dataset.collate(
        samples=[{'id': -1, 'source': tokens}],  # bsz = 1
        pad_idx=task.source_dictionary.pad(),
        eos_idx=task.source_dictionary.eos(),
        left_pad_source=False,
        input_feeding=False,
    )

    # Feed batch to the model and get predictions
    preds = model(**batch['net_input'])

    # Print top 3 predictions and their log-probabilities
    top_scores, top_labels = preds[0].topk(k=3)
    for score, label_idx in zip(top_scores, top_labels):
        label_name = task.target_dictionary.string([label_idx])
        print('({:.2f})\t{}'.format(score, label_name))