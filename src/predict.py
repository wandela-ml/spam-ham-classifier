import joblib
from src.preprocessing import clean_text


model = joblib.load("models/spam_classifier.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

def predict_message(message):
    clean_message = clean_text(message)
    message_vector = vectorizer.transform([clean_message])
    prediction = model.predict(message_vector)

    return int(prediction[0])

if __name__== "__main__":
    message = input("Enter an SmS message: ")
    result = predict_message(message)
    print(f"\n prediction: {result}")