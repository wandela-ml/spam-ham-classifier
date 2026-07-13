import re
import string


from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import nltk

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

# initialize our objects
stop_words = set(stopwords.words('english'))
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