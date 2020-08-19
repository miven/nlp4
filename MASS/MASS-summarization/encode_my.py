import argparse
import contextlib
import sys

from collections import Counter
from multiprocessing import Pool

from pytorch_transformers import BertTokenizer

'''
还是把这个脚本写成自己的可以debug的版本.
'''
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputs",
        nargs="+",
        default=['-'],
        help="input files to filter/encode",
    )
    parser.add_argument(
        "--outputs",
        nargs="+",
        default=['-'],
        help="path to save encoded outputs",
    )
    parser.add_argument(
        "--keep-empty",
        action="store_true",
        help="keep empty lines",
    )
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    '''
    // docker 中已经把所有需要的数据都放到了/wikitext-103-raw  里面.
    '''
    args.inputs=[]
    args.outputs=[]
    for SPLIT in ['train', 'valid', 'test']:
        args.inputs.append('/wikitext-103-raw/wiki.'+SPLIT+'.raw')
        args.outputs.append('/mono/'+SPLIT+'.txt')
    assert len(args.inputs) == len(args.outputs), \
        "number of input and output paths should match"

    with contextlib.ExitStack() as stack:
        inputs = [
            stack.enter_context(open(input, "r", encoding="utf-8"))
            if input != "-" else sys.stdin
            for input in args.inputs
        ]
        outputs = [
            stack.enter_context(open(output, "w", encoding="utf-8"))
            if output != "-" else sys.stdout
            for output in args.outputs
        ]

        encoder = MultiprocessingEncoder(args) # 他妹的多进程写的程序没法debug
        # pool = Pool(args.workers, initializer=encoder.initializer)
        # encoded_lines = pool.imap(encoder.encode_lines, zip(*inputs), 100)

        # 把上面的多进程改成单进程,方便debug.
        encoder.initializer()
        encoded_lines=encoder.encode_lines(inputs)

        stats = Counter()
        for i, (filt, enc_lines) in enumerate(encoded_lines, start=1):
            if filt == "PASS":
                for enc_line, output_h in zip(enc_lines, outputs):
                    print(enc_line, file=output_h)
            else:
                stats["num_filtered_" + filt] += 1
            if i % 10000 == 0:
                print("processed {} lines".format(i), file=sys.stderr)

        for k, v in stats.most_common():
            print("[{}] filtered {} lines".format(k, v), file=sys.stderr)


class MultiprocessingEncoder(object):

    def __init__(self, args):
        self.args = args

    def initializer(self):
        global bpe   # 使用.
        bpe = BertTokenizer.from_pretrained('bert-base-uncased')

    def encode(self, line):
        global bpe
        subword = bpe._tokenize(line)
        return subword

    def decode(self, tokens):
        global bpe
        return bpe.decode(tokens)

    def encode_lines(self, lines):
        """
        Encode a set of lines. All lines will be encoded together.
        """
        enc_lines = []
        for line in lines:
            line = line.strip()
            if len(line) == 0 and not self.args.keep_empty:
                return ["EMPTY", None]
            tokens = self.encode(line)
            enc_lines.append(" ".join(tokens))
        return ["PASS", enc_lines]

    def decode_lines(self, lines):
        dec_lines = []
        for line in lines:
            tokens = map(int, line.strip().split())
            dec_lines.append(self.decode(tokens))
        return ["PASS", dec_lines]


if __name__ == "__main__":
    main()

    '''
    
    running:
    fairseq-preprocess \
    --user-dir mass --only-source --task masked_s2s \
    --trainpref /mono/train.txt --validpref /mono/valid.txt --testpref /mono/test.txt \
    --destdir processed --srcdict dict.txt --workers 60
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    '''
