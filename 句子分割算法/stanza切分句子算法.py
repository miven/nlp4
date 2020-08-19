import stanza           # 看看这个stanfu算法吧.
stanza.download('en')       # This downloads the English models for the neural pipeline
nlp = stanza.Pipeline('en') # This sets up a default neural pipeline in English
doc = nlp("Barack Obama was born in U.S.A.he was elected president in 2008.")
print(len(doc.sentences))
# print(doc.sentences)
