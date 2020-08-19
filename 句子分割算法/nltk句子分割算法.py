import nltk
import nltk.data
'''
这个破算法不咋地啊,这都拆不出来.这个可以弃用了!!!!!!!!!!!!!
'''
nltk.download('punkt')
def splitSentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences


if __name__ == '__main__':
    print(
    splitSentence("My name is Tom.i am a boy.i like soccer!"))