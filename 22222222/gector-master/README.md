

2020-07-07,17点48


文本纠错改进:

    经过了昨天的评测,发现之前论文实现的模型有拼写无法纠正,和复杂单复数无法辨别的问题.
    后续打算从 1. 模型结构. 把linear改成复杂的
    2. 加错误类型.
    目前已经从2方案上调通了.代码在train_finetune_latest2.py 直接运行即可.
    已经封装好了,对应的日志信息, 运行后就会打印信息.方便查看是否学习到应该学到的tag信息.
    
    3.对于拼写错误可以类似上面来搞.但是,如果1个词对应多重改法.那就目前没办法实现了.
    因为如果对应多种改法,就需要拓展tag.
    
    4.代码目前比较复杂,建议不要随便动配置文件包括所有的txt文件和vocab文件.很容易出bug.















关于数据集的问题:
发现数据集里面一个行文本中存在多个句子的情况.并且存在句号前后缺少空格的情况.都会导致数据集质量不高.所以需要预处理














labels文件说明:

$KEEP
$DELETE
$TRANSFORM_CASE_CAPITAL
$APPEND_the
$APPEND_,
$APPEND_a
$TRANSFORM_VERB_VB_VBZ
$TRANSFORM_AGREEMENT_PLURAL
$TRANSFORM_CASE_LOWER
$TRANSFORM_VERB_VB_VBN
$REPLACE_the
$REPLACE_a


比如这些东西:
第一个就是keep current token
第二个就是delete currernt token
第6个就是在current的右边添加a
第11个就是替换当前位置的token为the


总结: keep 一个
delete 1个
replace 3892
append 1167

transform 27
merge 2

共计:5000


经过代码修改,如果抛开网络不修改的话.
这个网络是后续可以继续做优化的一个点.我们为了目前项目最快finetune.我写了train_finetune.py
这个代码效果是不改变网络的结构,还是使用xlnet预训练加一个最后的Distributed time linear层.就
得到了训练之后的model.然后把这个model 替换到predict里面的路径就可以使用新模型了.
为什么要进行finetune.
因为任务场景下数据集特征不一样,做finetune可以让准确率再特定 场景下边的更高.


再次进行傻瓜化集成.train后,直接打印效果.其实也不用,直接看训练时候打印的accuracy 即可. 这个越准也就是效果越好.

再次傻瓜集成.直接输入平行预料.然后自动preprocess_data.py 输出output.txt ,然后自动finetune. 打印评价accuracy和loss ,保存模型. 打印模型保存地址.
集成后的代码是train_finetune_latest.py !!!!!!!!!!!!!!!

使用的时候直接在predict代码中替换对应模型路径即可!!!!!!!!!!!!











原始地址.
https://github.com/grammarly/gector







2020-06-17,12点53

已经跑通了.
运行方式, python3 predict.py 即可
输入写入1里面,输出会在2里面.

compared to the origin , i fixed a bug on  273line in gec_model.py
fixed bug on 35 line in helpers.py


pip install allennlp -timeout=1000000000000000

allennlp==0.8.4   注意要安装旧版本的allennlp
默认安装的1.0版本,会不兼容.

scikit-learn==0.20.0






生成假文本的代码:
https://github.com/zhangbo2008/fairseq-gec/blob/master/333/PIE-master/errorify/errorifier.py





for i in :





# GECToR – Grammatical Error Correction: Tag, Not Rewrite

This repository provides code for training and testing state-of-the-art models for grammatical error correction with the official PyTorch implementation of the following paper:
> [GECToR – Grammatical Error Correction: Tag, Not Rewrite](https://arxiv.org/abs/2005.12592) <br>
> [Kostiantyn Omelianchuk](https://github.com/komelianchuk), [Vitaliy Atrasevych](https://github.com/atrasevych), [Artem Chernodub](https://github.com/achernodub), [Oleksandr Skurzhanskyi](https://github.com/skurzhanskyi) <br>
> Grammarly <br>
> [15th Workshop on Innovative Use of NLP for Building Educational Applications (co-located with ACL 2020)](https://sig-edu.org/bea/current) <br>

It is mainly based on `AllenNLP` and `transformers`.
## Installation
The following command installs all necessary packages:
```.bash
pip install -r requirements.txt
```
The project was tested using Python 3.7.

## Datasets
All the public GEC datasets used in the paper can be downloaded from [here](https://www.cl.cam.ac.uk/research/nl/bea2019st/#data).<br>
Synthetically created datasets can be generated/downloaded [here](https://github.com/awasthiabhijeet/PIE/tree/master/errorify).<br>
To train the model data has to be preprocessed and converted to special format with the command:
```.bash
python utils/preprocess_data.py -s SOURCE -t TARGET -o OUTPUT_FILE
```
## Pretrained models
<table>
  <tr>
    <th>Pretrained encoder</th>
    <th>Confidence bias</th>
    <th>Min error prob</th>
    <th>CoNNL-2014 (test)</th>
    <th>BEA-2019 (test)</th>
  </tr>
  <tr>
    <th>BERT <a href="https://grammarly-nlp-data-public.s3.amazonaws.com/gector/bert_0_gector.th">[link]</a></th>
    <th>0.10</th>
    <th>0.41</th>
    <th>63.0</th>
    <th>67.6</th>
  </tr>
  <tr>
    <th>RoBERTa <a href="https://grammarly-nlp-data-public.s3.amazonaws.com/gector/roberta_1_gector.th">[link]</a></th>
    <th>0.20</th>
    <th>0.50</th>
    <th>64.0</th>
    <th>71.5</th>
  </tr>
  <tr>
    <th>XLNet <a href="https://grammarly-nlp-data-public.s3.amazonaws.com/gector/xlnet_0_gector.th">[link]</a></th>
    <th>0.35</th>
    <th>0.66</th>
    <th>65.3</th>
    <th>72.4</th>
  </tr>
  <tr>
    <th>RoBERTa + XLNet</th>
    <th>0.24</th>
    <th>0.45</th>
    <th>66.0</th>
    <th>73.7</th>
  </tr>
  <tr>
    <th>BERT + RoBERTa + XLNet</th>
    <th>0.16</th>
    <th>0.40</th>
    <th>66.5</th>
    <th>73.6</th>
  </tr>
</table>

## Train model
To train the model, simply run:
```.bash
python train.py --train_set TRAIN_SET --dev_set DEV_SET \
                --model_dir MODEL_DIR
```
There are a lot of parameters to specify among them:
- `cold_steps_count` the number of epochs where we train only last linear layer
- `transformer_model {bert,distilbert,gpt2,roberta,transformerxl,xlnet,albert}` model encoder
- `tn_prob` probability of getting sentences with no errors; helps to balance precision/recall
- `pieces_per_token` maximum number of subwords per token; helps not to get CUDA out of memory

In our experiments we had 98/2 train/dev split.
## Model inference
To run your model on the input file use the following command:
```.bash
python predict.py --model_path MODEL_PATH [MODEL_PATH ...] \
                  --vocab_path VOCAB_PATH --input_file INPUT_FILE \
                  --output_file OUTPUT_FILE
```
Among parameters:
- `min_error_probability` - minimum error probability (as in the paper)
- `additional_confidence` - confidence bias (as in the paper)
- `special_tokens_fix` to reproduce some reported results of pretrained models

For evaluation use [M^2Scorer](https://github.com/nusnlp/m2scorer) and [ERRANT](https://github.com/chrisjbryant/errant).
## Citation
If you find this work is useful for your research, please cite our paper:
```
@misc{omelianchuk2020gector,
    title={GECToR -- Grammatical Error Correction: Tag, Not Rewrite},
    author={Kostiantyn Omelianchuk and Vitaliy Atrasevych and Artem Chernodub and Oleksandr Skurzhanskyi},
    year={2020},
    eprint={2005.12592},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```
