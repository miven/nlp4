import transformers
import torch
import os
import json
import random
import argparse
import numpy as np
from datetime import datetime
from torch.nn import DataParallel
from tqdm import tqdm
'''

2020-08-03,16点40


首先研究一下这个不使用中文预训练的模型,而是从头开始训练整个gpt2
的代码.看看如何跑通.


注意版本是这个.
transformers==2.1.1



gpt2学习:
https://www.cnblogs.com/zhongzhaoxie/p/13064404.html


'''
'''
如果训练材料是全部堆在一起不分篇章的话用这个文件

下面我们就利用这个开始写我们自己的gpt2生成中文文本的代码.



这里面是开源的gpt2 中文

https://spaces.ac.cn/archives/7292

https://colab.research.google.com/github/imcaspar/gpt2-ml/blob/master/pretrained_model_demo.ipynb


https://github.com/imcaspar/gpt2-ml 
'''


def build_files(raw_data_path, tokenized_data_path, full_tokenizer, num_pieces):
    with open(raw_data_path, 'r', encoding='utf8') as f:
        print('reading lines')
        lines = json.load(f)
        lines = [line.replace('\n', ' [SEP] ') for line in lines]  # 用[SEP]表示换行, 段落之间使用SEP表示段落结束
    single = ''.join(lines)
    len_single = len(single)
    if not os.path.exists(tokenized_data_path):
        os.makedirs(tokenized_data_path)  # makedirs递归的创建目录.
    for i in tqdm(range(num_pieces)):
        single_ids = full_tokenizer.convert_tokens_to_ids(
            full_tokenizer.tokenize(single[len_single // num_pieces * i: len_single // num_pieces * (i + 1)           ]))
        with open(tokenized_data_path + 'tokenized_train_{}.txt'.format(i), 'w') as f:
            for id in single_ids[:-1]:
                f.write(str(id) + ' ') # 每一个字符之间用空格间隔.
            f.write(str(single_ids[-1]))
            f.write('\n') # 这里面的编码里面没有任何的空格.

    print('finish')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', default='0,1,2,3', type=str, required=False, help='设置使用哪些显卡')
    parser.add_argument('--model_config', default='config/model_config.json', type=str, required=False,
                        help='选择模型参数')
    parser.add_argument('--tokenizer_path', default='cache/vocab_small.txt', type=str, required=False, help='选择词库')
    parser.add_argument('--raw_data_path', default='data/train.json', type=str, required=False, help='原始训练语料')
    parser.add_argument('--tokenized_data_path', default='data/tokenized/', type=str, required=False,
                        help='tokenized语料存放位置')
    parser.add_argument('--raw', action='store_true', help='是否先做tokenize')
    parser.add_argument('--epochs', default=5, type=int, required=False, help='训练循环')
    parser.add_argument('--batch_size', default=8, type=int, required=False, help='训练batch size')
    parser.add_argument('--lr', default=1.5e-4, type=float, required=False, help='学习率')
    parser.add_argument('--warmup_steps', default=2000, type=int, required=False, help='warm up步数')
    parser.add_argument('--log_step', default=1, type=int, required=False, help='多少步汇报一次loss')
    parser.add_argument('--stride', default=768, type=int, required=False, help='训练时取训练数据的窗口步长')
    parser.add_argument('--gradient_accumulation', default=1, type=int, required=False, help='梯度积累')
    parser.add_argument('--fp16', action='store_true', help='混合精度')
    parser.add_argument('--fp16_opt_level', default='O1', type=str, required=False)
    parser.add_argument('--max_grad_norm', default=1.0, type=float, required=False)
    parser.add_argument('--num_pieces', default=1, type=int, required=False, help='将训练语料分成多少份')
    parser.add_argument('--output_dir', default='model/', type=str, required=False, help='模型输出路径')
    parser.add_argument('--pretrained_model', default='', type=str, required=False, help='模型训练起点路径')
    parser.add_argument('--segment', action='store_true', help='中文以词为单位')

    '''
    配置参数-------------------------------------------------------------------
    '''
    args = parser.parse_args()
    args.device='1'
    args.batch_size=5
    from tokenizations import tokenization
    proj_root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    vocab_file_path ="tokenizations/clue-vocab.txt"
#使用预训练里面的词典进行编码
    text='我是一个人'
    tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file_path, do_lower_case=True)
    line = tokenization.convert_to_unicode(text)
    bert_tokens = tokenizer.tokenize(line)
    encoded = tokenizer.convert_tokens_to_ids(bert_tokens)

# 下面关注一下数据集的写法.
    args.raw=True
    args.raw_data_path='172166.txt'         # -small是小的版本
    args.epochs=200
    args.output_dir='model/'          # 结果存到e盘的final_model
    args.num_pieces=10      # 结果存到e盘的final_model
    from pre_data_byOnlyOneBook import get_data as get_data
    name2=args.raw_data_path.split('.')[0]
    get_data(name2+'.txt',name2+'.json')
    # 下面使用166893.json即可.
    '''
    ------------------------------------------------------------------------------
    '''







    #---------------配置完毕
    print('args:\n' + args.__repr__())
    if args.segment:
        from tokenizations import tokenization_bert_word_level as tokenization_bert
    else:
        from tokenizations import tokenization_bert
    os.environ["CUDA_VISIBLE_DEVICES"] = args.device  # 此处设置程序使用哪些显卡
    model_config = transformers.modeling_gpt2.GPT2Config.from_json_file(args.model_config)# 这个参数很重要,表示一句话的长度.
    print('config:\n' + model_config.to_json_string())
    n_ctx = model_config.n_ctx
    # full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=args.tokenizer_path)
    full_tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file_path, do_lower_case=True)
    '''
    full_tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file_path, do_lower_case=True)
    '''




    '''
    直接使用gpt2的tokenizer
    '''



    full_tokenizer.max_len = 999999
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print('using device:', device)

    raw_data_path = args.raw_data_path
    tokenized_data_path = args.tokenized_data_path
    raw = args.raw  # 选择是否从零开始构建数据集
    epochs = args.epochs
    batch_size = args.batch_size
    lr = args.lr
    warmup_steps = args.warmup_steps
    log_step = args.log_step
    stride = args.stride
    gradient_accumulation = args.gradient_accumulation
    fp16 = args.fp16  # 不支持半精度的显卡请勿打开
    fp16_opt_level = args.fp16_opt_level
    max_grad_norm = args.max_grad_norm
    num_pieces = args.num_pieces
    output_dir = args.output_dir
#  'data/tokenized/'  编码之后的东西放在这里.
    if raw:
        print('building files')
        build_files(raw_data_path=name2+'.json', tokenized_data_path=tokenized_data_path, full_tokenizer=full_tokenizer,
                    num_pieces=num_pieces)
        print('files built')

    if not args.pretrained_model:
        model = transformers.modeling_gpt2.GPT2LMHeadModel(config=model_config)
    else:
        model = transformers.modeling_gpt2.GPT2LMHeadModel.from_pretrained(args.pretrained_model)
    model.train()
    model.to(device)
    multi_gpu = False
    full_len = 0
    print('calculating total steps')
    for i in tqdm(range(num_pieces)):
        with open(tokenized_data_path + 'tokenized_train_{}.txt'.format(i), 'r') as f:
            full_len += len([int(item) for item in f.read().strip().split()])
    import math
    total_steps = math.ceil(full_len / stride * epochs / batch_size / gradient_accumulation)
    print('total steps = {}'.format(total_steps))

    optimizer = transformers.AdamW(model.parameters(), lr=lr, correct_bias=True)
    scheduler = transformers.WarmupLinearSchedule(optimizer, warmup_steps=warmup_steps,
                                                          t_total=total_steps)
    if fp16:
        try:
            from apex import amp
        except ImportError:
            raise ImportError("Please install apex from https://www.github.com/nvidia/apex to use fp16 training.")
        model, optimizer = amp.initialize(model, optimizer, opt_level=fp16_opt_level)

    if torch.cuda.device_count() > 1:
        print("Let's use", torch.cuda.device_count(), "GPUs!")
        model = DataParallel(model)
        multi_gpu = True
    print('starting training')
    running_loss = 0
    for epoch in range(epochs):
        print('epoch {}'.format(epoch + 1))
        now = datetime.now()
        print('time: {}'.format(now))
        x = np.linspace(0, num_pieces - 1, num_pieces, dtype=np.int32)
        random.shuffle(x)
        piece_num = 0
        loss_save=[]
        for i in x:
            with open(tokenized_data_path + 'tokenized_train_{}.txt'.format(i), 'r') as f:
                line = f.read().strip()
            tokens = line.split()
            tokens = [int(token) for token in tokens]
            start_point = 0
            samples = []
            while start_point < len(tokens) - n_ctx:  # n_ctx 表示上下文的长度.
                samples.append(tokens[start_point: start_point + n_ctx])
                start_point += stride
            if start_point < len(tokens): # 拼接上最后一个例子.
                samples.append(tokens[len(tokens)-n_ctx:])
            random.shuffle(samples)
            for step in range((len(samples) // batch_size)+1):# 多跑一个

                #  prepare data
                #先判断是否超界,如果超界就表示最后一个组不成batch,所以break
                if step * batch_size>len(samples)-1:
                    break
                batch = samples[step * batch_size: (step + 1) * batch_size]


                batch_labels = []
                batch_inputs = []
                for ids in batch:
                    int_ids_for_labels = [int(x) for x in ids]
                    int_ids_for_inputs = [int(x) for x in ids]
                    batch_labels.append(int_ids_for_labels)
                    batch_inputs.append(int_ids_for_inputs)
                batch_labels = torch.tensor(batch_labels).long().to(device)
                batch_inputs = torch.tensor(batch_inputs).long().to(device)

                #  forward pass       居然输入输出都一样????????很奇怪这个模型.

                '''
                下面为了对比,把ctrl的模型写这里:
                
                
                    flag_input, inputs = numericalize(domain+tokenized_train_text[i:i+seq_length])  # 注意输入要牵头加上domain.
                    flag_output, outputs = numericalize(tokenized_train_text[i:i+seq_length+1])  # ctrl算法输入是 i:j 输出是i:j+1 
                    
                    
                    研究一下这个数据的问题:
                    https://www.cnblogs.com/wwj99/p/12503545.html
                    
                    好像还真是,样本和标签一样.
                '''
                outputs = model.forward(input_ids=batch_inputs, labels=batch_labels)
                loss, logits = outputs[:2]

                #  get loss
                if multi_gpu:
                    loss = loss.mean()
                if gradient_accumulation > 1:
                    loss = loss / gradient_accumulation

                #  loss backward
                if fp16:
                    with amp.scale_loss(loss, optimizer) as scaled_loss:
                        scaled_loss.backward()
                        torch.nn.utils.clip_grad_norm_(amp.master_params(optimizer), max_grad_norm)
                else:
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)

                #  optimizer step
                if (step + 1) % gradient_accumulation == 0:
                    running_loss += loss.item()
                    optimizer.step()
                    optimizer.zero_grad()
                    scheduler.step()
                if (step + 1) % log_step == 0:
                    print('now time: {}:{}. Step {} of piece {} of epoch {}, loss {}'.format(
                        datetime.now().hour,
                        datetime.now().minute,
                        (step + 1) // gradient_accumulation,
                        piece_num,
                        epoch + 1,
                        running_loss / log_step))
                    loss_save.append(running_loss / log_step)
                    running_loss = 0
            piece_num += 1
        #--------------检测是否提前退出
        last=loss_save[:10]
        avg1=sum(last)/10
        #如果全在avg1上下百分之5以内就停止:
        last=np.array(last)
        avg1=np.array(avg1)
        tmp=np.all(last >=avg1*0.97) and np.all(last>=avg1*1.03)
        if len(last)>=10 and tmp and loss_save[-1]<0.05:
            break

#--------------------



    print('training finished')
    if not os.path.exists(output_dir + 'final_model'):
        os.makedirs(output_dir + 'final_model')
    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(output_dir + 'final_model')
    # torch.save(scheduler.state_dict(), output_dir + 'final_model/scheduler.pt')
    # torch.save(optimizer.state_dict(), output_dir + 'final_model/optimizer.pt')


if __name__ == '__main__':
    main()
