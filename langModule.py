import nltk
from nltk.stem import PorterStemmer

stop_words = list(nltk.corpus.stopwords.words('english'))
stemmer = PorterStemmer()

def get_tokens(text, alpha=True):
    tokens = nltk.word_tokenize(text)
    if alpha:
        return [token.lower() for token in tokens if token.isalpha()]
    return [token.lower() for token in tokens if token.isalnum()]

def remove_stop_words(tokens):
    return [item for item in tokens if item not in stop_words]

def get_stems(tokens):
    return [stemmer.stem(token) for token in tokens]

def proccess_text(text, stemming=False, alpha=True):
    tokens = get_tokens(text, alpha)
    tokens = remove_stop_words(tokens)
    if stemming:
        tokens = get_stems(tokens)
    return tokens

def get_term_docIDs(text, docID, stemming=False, alpha=True):
    tokens = proccess_text(text, stemming, alpha)
    return [(token, docID) for token in tokens]