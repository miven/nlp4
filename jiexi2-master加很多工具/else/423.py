import numpy as np
tmp=np.array([3,5,2,1,3])
vec1=np.array([3,1,1,2,1])








from gensim.models import word2vec

sentences = word2vec.Text8Corpus("./text8")

model = word2vec.Word2Vec(sentences,size=200)


model.most_similar(["boy"], topn=3)
# or
model.most_similar("boy", topn=3)

# gensim.models.keyedvectors.WordEmbeddingsKeyedVectors.



from gensim.models import Word2Vec
# model = Word2Vec.load(path/to/your/model)
model.similarity('france', 'spain')
