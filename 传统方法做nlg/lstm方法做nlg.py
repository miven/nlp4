'''
https://www.jianshu.com/p/1bb7bad11733

'''
from keras import Sequential
from keras.layers import Bidirectional, LSTM, Dense
from keras.utils import to_categorical
from keras_preprocessing.sequence import pad_sequences
import numpy as np

corpus = '''
这一生原本一个人，你坚持厮守成我们，却小小声牵着手在默认。
感动的眼神说愿意，走进我的人生。
进了门开了灯一家人，盼来生依然是一家人。
确认过眼神，我遇上对的人。
我挥剑转身，而鲜血如红唇。
前朝记忆渡红尘，伤人的不是刀刃，是你转世而来的魂。
青石板上的月光照进这山城，我一路的跟你轮回声，我对你用情极深。
谁在用琵琶弹奏一曲东风破，枫叶将故事染色，结局我看透。
篱笆外的古道我牵着你走过，荒烟漫草的年头，就连分手都很沉默。
'''

class TextGenerate():
    def __init__(self, window=3, corpus=corpus):
        self.window = window
        self.corpus = corpus
        self.char2id = None
        self.id2char = None
        self.char_length = 0


    def load_data(self):
        X = []
        Y = []
        # 将语料按照\n切分为句子
        corpus = self.corpus.strip().split('\n')
        # 获取所有的字符作为字典
        chrs = set(self.corpus.replace('\n', ''))
        chrs.add('UNK')
        self.char_length = len(chrs)
        self.char2id = {c: i for i, c in enumerate(chrs)}
        self.id2char = {i: c for c, i in self.char2id.items()}
        for line in corpus:
            x = [[self.char2id[char] for char in line[i: i + self.window]] for i in range(len(line) - self.window)]
            y = [[self.char2id[line[i + self.window]]] for i in range(len(line) - self.window)]
            X.extend(x)
            Y.extend(y)
        # 转为one-hot
        X = to_categorical(X)
        Y = to_categorical(Y)
        return X, Y

    def build_model(self):
        model = Sequential()
        model.add(Bidirectional(LSTM(100,return_sequences=True)))
        model.add(Bidirectional(LSTM(200)))
        model.add(Dense(self.char_length, activation='softmax'))
        model.compile('adam', 'categorical_crossentropy')
        self.model = model


    def train_model(self,X,Y,epochs):
        self.model.fit(X, Y, epochs=epochs, verbose=1)
        self.model.save('model.model')
    def predict(self,sentence):
        input_sentence = [self.char2id.get(char,self.char2id['UNK']) for char in sentence]
        input_sentence = pad_sequences([input_sentence],maxlen=self.window)
        input_sentence = to_categorical(input_sentence,num_classes=self.char_length)
        predict = self.model.predict(input_sentence)
        # 本文为了方便 直接取使用最大概率的值，并非绝对，采样的方式有很多种，自行选择
        return self.id2char[np.argmax(predict)]



#---------------调用.
# 以5切分
window = 5
text_generate = TextGenerate(window,corpus)
X,Y = text_generate.load_data()
text_generate.build_model()
text_generate.train_model(X,Y,12)
# text_generate.load_model()
input_sentence = '确认1'
result = input_sentence
#在构建语料的过程中，设置了每次只预测一个词，为了生成完成的一句话，需要进行循环预测
while not result.endswith('。'):
    predict = text_generate.predict(input_sentence)
    result += predict
    input_sentence += predict
    input_sentence = input_sentence[len(input_sentence)-(window if len(input_sentence)>window else len(input_sentence)):]
    print(result)
