import argparse
import torch
from utils.helpers import read_lines
from gector.gec_model import GecBERTModel

from utils.set_helper import correct
def predict_for_file(input_file, output_file, model, batch_size=32):
    test_data = read_lines(input_file)
    predictions = []
    cnt_corrections = 0
    batch = []
    test_data=[correct(i) for i in test_data]


    for sent in test_data:
        batch.append(sent.split())
        if len(batch) == batch_size:
            preds, cnt = model.handle_batch(batch)
            predictions.extend(preds)
            cnt_corrections += cnt
            batch = []
        print("处理了一个batch")
    if batch:
        preds, cnt = model.handle_batch(batch)
        predictions.extend(preds)
        cnt_corrections += cnt

    with open(output_file, 'w') as f:
        f.write("\n".join([" ".join(x) for x in predictions]) + '\n')
    return cnt_corrections,test_data,predictions


def main(args):
    # get all paths
    model = GecBERTModel(vocab_path=args.vocab_path,
                         model_paths=args.model_path,
                         max_len=args.max_len, min_len=args.min_len,
                         iterations=args.iteration_count,
                         min_error_probability=args.min_error_probability,
                         min_probability=args.min_error_probability,
                         lowercase_tokens=args.lowercase_tokens,
                         model_name=args.transformer_model,
                         special_tokens_fix=args.special_tokens_fix,
                         log=False,
                         confidence=args.additional_confidence,
                         is_ensemble=args.is_ensemble,
                         weigths=args.weights)
# 模型运行即可.
    cnt_corrections,wenben1,wenben2 = predict_for_file(args.input_file, args.output_file, model,
                                       batch_size=args.batch_size)
    '''
    "explain": 纠错说明, 
       "location": 错误单词位置,
         "sensitive": 错误文本,
      "expect": 推荐文本, 
      "level": 错误级别（0-2 越大越严重）, 
      "errtype": 错误类型,
       'shortsentence'
    '''
    error_inform=[]
    wenben3=[i.split(' ') for i in wenben1]
    for i in range(len(wenben3)):
        error=[]
        tmp1=wenben3[i]
        tmp2=wenben2[i]
        for j in range(min(len(tmp1),len(tmp2))):
            if tmp1[j]!=tmp2[j]:
                error.append({
                    'explain':'gec',
                    'location':j,
                    'sensitive':tmp1[j],
                    'expect':tmp2[j],
                    'level':1,
                    'errtype':'gec',
    'shortsentence':tmp1[j-1:j+1]
                })
        error_inform.append(error)
    print(error_inform)





    # evaluate with m2 or ERRANT
    print(f"Produced overall corrections: {cnt_corrections}")
    print("都预测完毕")


if __name__ == '__main__':
    # read parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path',
                        help='Path to the model file.', nargs='+',
                        required=False)
    parser.add_argument('--vocab_path',
                        help='Path to the model file.',
                        default='data/output_vocabulary'  # to use pretrained models
                        )
    parser.add_argument('--input_file',
                        help='Path to the evalset file',
                        required=False)
    parser.add_argument('--output_file',
                        help='Path to the output file',
                        required=False)
    parser.add_argument('--max_len',
                        type=int,
                        help='The max sentence length'
                             '(all longer will be truncated)',
                        default=50)
    parser.add_argument('--min_len',
                        type=int,
                        help='The minimum sentence length'
                             '(all longer will be returned w/o changes)',
                        default=3)  # 句子单词如果比3个还少,就错了. 3个单词看做正常的句子.太短的句子一般不会出错. 或者后续设置为0, 也可以试试效果.
    parser.add_argument('--batch_size',
                        type=int,
                        help='The size of hidden unit cell.',
                        default=128)
    parser.add_argument('--lowercase_tokens',
                        type=int,
                        help='Whether to lowercase tokens.',
                        default=0)
    parser.add_argument('--transformer_model',
                        choices=['bert', 'gpt2', 'transformerxl', 'xlnet', 'distilbert', 'roberta', 'albert'],
                        help='Name of the transformer model.',
                        default='xlnet') # 网上只能下载到最好的就是xxlnet
    parser.add_argument('--iteration_count',
                        type=int,
                        help='The number of iterations of the model.',
                        default=5)
    parser.add_argument('--additional_confidence',
                        type=float,
                        help='How many probability to add to $KEEP token.',
                        default=0)
    parser.add_argument('--min_probability',
                        type=float,
                        default=0.0)
    parser.add_argument('--min_error_probability',
                        type=float,
                        default=0.0)
    parser.add_argument('--special_tokens_fix',
                        type=int,
                        help='Whether to fix problem with [CLS], [SEP] tokens tokenization. '
                             'For reproducing reported results it should be 0 for BERT/XLNet and 1 for RoBERTa.',
                        default=0)
    parser.add_argument('--is_ensemble',
                        type=int,
                        help='Whether to do ensembling.', # 是否进行集成学习.就是事用多模型.
                        default=0)
    parser.add_argument('--weights',
                        help='Used to calculate weighted average', nargs='+',
                        default=None)
    args = parser.parse_args()

    '''
    手动写死参数,方便debug.
    '''

    # ---------下面这2个是我改进后的配置
    args.model_path=['tmpModel2/model.th']  # 需要传入数组.
    args.vocab_path='tmpModel2/vocabulary'


    # ----------如果想用默认模型需要配置成如下:
    '''
    args.model_path=['/xlnet_0_gector.th']  # 需要传入数组.
    args.vocab_path='data/output_vocabulary'
    '''






    # 下面使用论文里面的参数.
    args.confidence=0  # ps: 这个参数写0,就是原始的配置.越接近1表示修改的越严格,修改的越少.
    args.additional_confidence=0.35  #根据官网提供的设置好参数.同样也是越小,表示改动越大.
    args.min_error_probability=0.66  #根据官网提供的设置好参数.同样也是越小,表示改动越大.






    # 己定义的一个参数,如果改动小于这个数,说明改动意义不大,强制把不动原始位置的单词.
    with open('conf','w') as f :
        f.write(str(args.confidence))
    with open('conf',) as f :
        tmp=float(f.readlines()[0])
    # 下面改成我们自己训练得到的模型.
    # args.model_path=['tmpModel/model.th']  # 需要传入数组.

    args.input_file='1'
    args.output_file='2'
    main(args)
    '''
    调参:1里面最后一个句子,也就是index 为4 的.
    输出为class_probabilities_labels
    位置7, 修改为了17. 对一个就是$REPLACE_in 当前位置替换为in 
我们看他的概率多大.   概率是0.83.   我修改为0.85试试. 也就是置信度.
    '''














