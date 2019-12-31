
from spacy.lang.fr import French
from nltk.tokenize import RegexpTokenizer

def RecupererTextTokenSansPonctuation(fichier):
#Import Package French langages
    Langue = French()
    f = fichier
    tokenizer = RegexpTokenizer(r'\w+')
    doc = Langue(f.read())
    filtered_sent = []
    for word in doc:
            if word.text:
                filtered_sent.append(word)
# delete all and save just text
    return str(tokenizer.tokenize(str(filtered_sent)))

