import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources only if they are missing
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

try:
    nltk.data.find("corpora/omw-1.4")
except LookupError:
    nltk.download("omw-1.4")

# initialize our objects
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# first create a function that accepts one text at a time
def clean_text(text):
    text = text.lower()
    # remove special characters a numbers 
    text = re.sub(r'[^a-z\s]', '', text)

    #tokenize the sentence 
    words = text.split()


    # remove stopwords and lemmatize
    cleaned_words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words

    ]
    return ' '.join(cleaned_words)
if __name__== "__main__":
    sample = "This is an Example!!! of TEXT preprocessing with 123 numbers."
    print(clean_text(sample))