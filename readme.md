
huggingface:使用说明:
找model:类别为
   1.sentence classification : gleu任务
   2.toekn calssification: ner任务
   3.qa:qa任务





本仓库,项目汇总说明:


对于albert做词向量finetune,得到更好的刻画:!!!!!!!!!!!!
知识图谱项目/kg加深度学习/词向量finetune/对albert模型做finetune让他的词向量距离效果更好.py



# word2vec 做中文, 根本不能用. oov问题.太严重.       中华,------中,   华 拆开语义就完全不一样.









albert词向量究极版本:

知识图谱项目/kg加深度学习/huizong2使用的是albert大版本.py







中文qa模型:
albert使用/中文qa模型!!!!!!!!!!!!!!!!!!!.py


注意函数返回值有propability,自己设置一个阈值,如果小于这个值,就表示答案在text中不存在,返回error即可.




中文qa finetune模型 :
albert使用/中文qa模型!Finetune.py







英文qa finetune代码:
albert使用/ImportantExmapleForFinetune.py


英文qa:
albert使用/ImportantExmaple.py




squad核心转化函数:
C:\Users\Administrator\.PyCharm2019.3\system\remote_sources\-456540730\-337502517\transformers\data\processors\squad.py








智能问答kg解决方案实施:
知识图谱项目/kg加深度学习/huizong.py







albert的配置:

huggingface项目中重要例子/transformers/src/transformers/configuration_albert.py











所有的albert使用model,看接哪个头适合.
C:\Users\Administrator\.PyCharm2019.3\system\remote_sources\-456540730\-337502517\transformers\modeling_albert.py








经典textrank算法做ext:
中国搜索/TextRank4ZH-master/example/example01.py









人脸/facenet-pytorch/examples

是人脸识别项目包含识别,检测,和训练代码.










22222222/gector-master2/train_finetune_latest3.py
 
     是 纠错最终版本(对原有开源模型进行了多种加强和bug修复.)



PreSumm2\src\train2.py 

     是extract 模型. 输入一段句子, 返回最有用的句子的index (index从0开始计数) (没有对原有开源模型进行加强,只是简单的函数封装.)


PreSumm2/src/train3.py 

    是abs模型.     输入一段句子, /output_abs.txt 会返回abs.
    



ctrl模型:

ctrl模型/ctrl原始代码/ctrl/pytorch_generation.py   

    这个直接运行就会返回所有生成的过程.


ctrl模型/run_generation (2)_for_ctrl.py

    更简洁的hugging-face generate代码.



ctrl模型/ctrl原始代码/ctrl/training_utils/training.py
    ctrl模型训练代码.还没调通.
    
    



一些其他的翻页和nlg任务:

    一些可以直接调用的nlp算法/一些语言之间的翻译和生成.md
    



中文nlg:
    gpt2做中文nlg/gpt2-ml-master/demo2.py
    直接运行即可.
    然后输入点汉子,就会后面续写.
    
    

中文nlg自己训练,加运行的代码:
gpt2做中文nlg/GPT2-Chinese-master修改为mega版本/README.md



python加速算法:

量化/main



































欢迎有爱的童鞋扫码


![Image text](https://raw.githubusercontent.com/zhangbo2008/fairseq-gec/latest_branch/11.png)"# nlp4" 
