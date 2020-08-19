from fairseq.models.masked_permutation_net import MPNet
mpnet = MPNet.from_pretrained(
	'checkpoints',
	'checkpoint_best.pt',
	data_name_or_path='RTE-bin',
	bpe='bert',
)


label_fn = lambda label: mpnet.task.label_dictionary.string(
    [label + mpnet.task.target_dictionary.nspecial]
)
ncorrect, nsamples = 0, 0
# mpnet.cuda()
mpnet.eval()
with open('glue_data/RTE/dev.tsv') as fin:
    fin.readline()
    for index, line in enumerate(fin):
        tokens = line.strip().split('\t')
        sent1, sent2, target = tokens[1], tokens[2], tokens[3]
        tokens = mpnet.encode(sent1, sent2)
        prediction = mpnet.predict('sentence_classification_head', tokens).argmax().item()
        prediction_label = label_fn(prediction)
        ncorrect += int(prediction_label == target)
        nsamples += 1
print('| Accuracy: ', float(ncorrect)/float(nsamples))