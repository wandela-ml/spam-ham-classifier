import joblib
import pandas as pd

from preprocessing import clean_text

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix, 
    recall_score,
    f1_score,
    precision_score
    )

DATA_PATH = "data/spam.csv"
MODEL_PATH = "models/spam_classifier.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

def load_data():
    """
    Load and clean the SMS spam dataset.

    Returns:
        pandas.DataFrame: A cleaned dataset with
        standardized column names.

    """

    df = pd.read_csv(DATA_PATH, encoding = 'latin-1')
    df = df.drop(
        columns=[
            "Unnamed: 2",
            "Unnamed: 3",
            "Unnamed: 4"
        ]
    )
    df = df.rename(columns={
        'v1': 'label',
        'v2': 'message'
    })
    return df

def prepare_data(df):
    """
    description: prepares the pre-cleaned data for training

    args: df (the cleaned dataframe from the load_data () function)

    Returns: A tuple, (X_train, X_test, y_train, y_test)
    """
    df['clean_message'] = df['message'].apply(clean_text)
    df["label"] = df["label"].map({
        "ham" : 0,
        "spam" : 1 
    })
    X= df['clean_message']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    return X_train, X_test, y_train, y_test


def vectorize_data(X_train, X_test):
    """
    responsibility: convert test to TF_IDF features (numerical data)
    args: X_train, X_test

    returns: tuple: vectorized X_train, vectorized X_test
    a fitted vectorizer
    """
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test  = vectorizer.transform(X_test)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    return X_train, X_test, vectorizer

def evaluate_model(model, X_test, y_test):
    """
    evaluate the trained models
    args: Model: trained machine learning model
        X_test: Vectorized test features
        y_test: The actual labels
    Returns: Precision
            accuracy
            f1_score
            recall
    """
    prediction = model.predict(X_test)
    precision = precision_score(y_test, prediction)
    recall = recall_score(y_test, prediction)
    f1 = f1_score(y_test, prediction)
    accuracy = accuracy_score(y_test, prediction)
    return (
        prediction,
        precision,
        recall,
        f1,
        accuracy
    )

def train_and_compare_models(X_train, X_test, y_train, y_test):
    """
    Role: trains the machine learning models. compares the performance of the machine learning models
    args: Vectorized X_train, vectorized X_test, actual train labels(y_train), actual test labels(y_test)
    returns: best model, best_model's f1 score and the best_model's prediction
    """
    models = {
        "naive_bayes": MultinomialNB(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "SVM": LinearSVC(),
        "Random Forest": RandomForestClassifier(random_state=42),
    }
    results =[]

    best_model = None
    best_f1 = 0
    best_prediction = None
    for name, model in models.items():
        model.fit(X_train, y_train)
        prediction, precision, recall, f1, accuracy = evaluate_model(model, X_test, y_test)
        results.append({
            "Model" : name,
            "Accuuracy": accuracy,
            "Prediction": prediction,
            "Precision": precision,
            "F1 Score": f1,
            "Recall Score": recall
            })
        if f1> best_f1:
            best_f1 = f1
            best_model = model
            best_prediction = prediction
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="F1 Score", ascending=False).reset_index(drop=True)
    cm = confusion_matrix(y_test, best_prediction)
    return best_model, results_df, cm

def save_model(best_model):
    """
    Role: Saves the trained model to disk. it saves the best model
    args: best model
    Returns: None
    """
    joblib.dump(best_model, MODEL_PATH)

def display_results(results_df, cm):
    """
    responsbility: Display the evaluation results
    args: results_df, confusion matrix (cm)
    Returns: None
    """
    print("\n Model Comparison\n")
    print(results_df)

    print("\n Confusion Matrix\n")
    print(cm)

def main():
    """Returns the complete model pipeline"""

    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)
    X_train, X_test, vectorizer = vectorize_data(X_train, X_test)
    best_model, results_df, cm = train_and_compare_models(
        X_train,
        X_test,
        y_train,
        y_test
    )
    save_model(best_model)
    display_results(results_df, cm)

if __name__ =="__main__":
    main()

