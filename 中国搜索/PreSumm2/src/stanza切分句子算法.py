import stanza
stanza.download('en')       # This downloads the English models for the neural pipeline
nlp = stanza.Pipeline('en') # This sets up a default neural pipeline in English
doc = nlp("Barack Obama was born in U.S.A. He was elected president in 2008.")
print(doc.sentences)
doc.sentences[0]