''' Translate input text with trained model. '''
# 训练好魔性后用这个代码来predict
import torch
import torch.utils.data
import argparse
from tqdm import tqdm

from dataset import collate_fn, TranslationDataset
from transformer.Translator import Translator
from preprocess import read_instances_from_file, convert_instance_to_idx_seq


# python translate.py -model trained.chkpt -vocab data/multi30k.atok.low.pt -src data/multi30k/test.en.atok -no_cuda


# 数据集已经下好在/tmp999里面了
def main():
    '''Main Function'''

    '''
    这个模型是从英语到德语.
    '''









    parser = argparse.ArgumentParser(description='translate.py')

    parser.add_argument('-model', required=False,
                        help='Path to model .pt file')
    parser.add_argument('-src', required=False,
                        help='Source sequence to decode (one line per sequence)')
    parser.add_argument('-vocab', required=False,
                        help='Source sequence to decode (one line per sequence)')
    parser.add_argument('-output', default='2',
                        help="""Path to output the predictions (each line will
                        be the decoded sequence""")
    parser.add_argument('-beam_size', type=int, default=5,
                        help='Beam size')
    parser.add_argument('-batch_size', type=int, default=30,
                        help='Batch size')
    parser.add_argument('-n_best', type=int, default=1,
                        help="""If verbose is set, will output the n_best
                        decoded sentences""")
    parser.add_argument('-no_cuda', action='store_true')



    #-vocab data/multi30k.atok.low.pt







    opt = parser.parse_args()
    opt.cuda = not opt.no_cuda
    opt.cuda=False
    opt.model='trained.chkpt'
    opt.src='1'
    opt.vocab='multi30k.atok.low.pt'
    # Prepare DataLoader
    preprocess_data = torch.load(opt.vocab)

    tmp1=preprocess_data['dict']['src']
    tmp2=preprocess_data['dict']['tgt']
    with open('55','w')as f:
        f.write(str(tmp1))

    with open('66','w',encoding='utf-8')as f:
        f.write(str(tmp2))





    preprocess_settings = preprocess_data['settings']
    test_src_word_insts = read_instances_from_file(
        opt.src,
        preprocess_settings.max_word_seq_len,
        preprocess_settings.keep_case)
    test_src_insts = convert_instance_to_idx_seq(
        test_src_word_insts, preprocess_data['dict']['src'])

    test_loader = torch.utils.data.DataLoader(
        TranslationDataset(
            src_word2idx=preprocess_data['dict']['src'],
            tgt_word2idx=preprocess_data['dict']['tgt'],
            src_insts=test_src_insts),
        num_workers=2,
        batch_size=opt.batch_size,
        collate_fn=collate_fn)

    translator = Translator(opt)

    with open(opt.output, 'w') as f:
        for batch in test_loader:
            all_hyp, all_scores = translator.translate_batch(*batch)
            for idx_seqs in all_hyp:
                for idx_seq in idx_seqs:
                    print(idx_seq)
                    pred_line = ' '.join([test_loader.dataset.tgt_idx2word[idx] for idx in idx_seq]) # 把id转化会text
                    f.write(pred_line + '\n')
    print('[Info] Finished.')

if __name__ == "__main__":
    main()
