### 转换成支持prepare_data 处理的数据格式，将文本生成1024长度的训练数据，stride为768
# python pre_data.py --filepath /data/home/share1/gpt2-ml-Finetune/data-mayun_xiugai --outfile /data/home/share1/gpt2-ml-Finetune/data/22.json
import re
import json
import argparse
import os
def get_data(filepath,outfile):

            filename =filepath
            f = open(filename, 'r', encoding='utf-8')
            data = f.read()
            strid = 768
            max_length = 1024
            data_list = []
            strat = 0
            end = 1024
            pattern1 =  r"^[^。！？]*"
            pattern2 = r'.*?[。！？]'            #[^...]	不在[]中的字符：[^abc] 匹配除了a,b,c之外的字符。
            # 我认为这个地方应该加上*后面加上? 来进行非贪婪匹配.否则句子都太长了.
            f_json = open(outfile,'w',encoding='utf-8')
            while strat<= len(data) :
                data_list.append((strat,end))
                if (data_list[-1][1]-data_list[-1][0])< max_length:
                    break
                strat += strid           # 就是滑动窗口.
                end = min(strat+max_length,len(data))
            tmp=[]
            for each in data_list:
                text = data[each[0]:each[1]]
                text2 = re.sub(pattern1,'',text)
                if text2.startswith('。') or text2.startswith('！') or text2.startswith('？'):
                    text3 =text2[1:]
                else:
                    text3 = text2
                #print(re.findall(pattern2,text3))
                text4_list = re.findall(pattern2,text3)
                text4 = '\n'.join(text4_list)
                tmp.append( text4)

            json_data = json.dumps(tmp,ensure_ascii=False)
            f_json.write(json_data)
            f_json.write('\n')
            f.close()
            print('finish')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', default='/data/home/share1/gpt2-ml-Finetune/data-mayun_xiugai', type=str, required=False, help='数据集目录地址')
    parser.add_argument('--outfile', default='/data/home/share1/gpt2-ml-Finetune/data/22.json', type=str, required=False,help='生成文件地址')
    args = parser.parse_args()


    args.filepath='166893.txt' # 拿倚天屠龙记当训练集
    args.outfile='166893.json'  # 输出也是同名的json
    print('args:\n' + args.__repr__())
    filepath = args.filepath
    outfile = args.outfile
    get_data(filepath,outfile)


if __name__ == '__main__':
    main()
