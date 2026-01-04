import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, f1_score


def chargement_data(chemin_csv):
    df = pd.read_csv(chemin_csv)
    return df["text"].tolist(), df["label"].tolist()

def vectorisation(texts):
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=5,
        max_df=0.85
    )
    X = vectorizer.fit_transform(texts)
    return X, vectorizer


def evaluation(model, X_train, X_test, y_train, y_test, vectorizer):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    model_name = model.__class__.__name__.lower()
    joblib.dump(model, f"model_{model_name}.joblib")
    joblib.dump(vectorizer, f"vectorizer_{model_name}.joblib")

    print(model.__class__.__name__)
    print(classification_report(y_test, y_pred, digits=3, zero_division=0))
    print("F1 macro:", f1_score(y_test, y_pred, average="macro"))
    print("-" * 60)


if __name__ == "__main__":
    texts, labels = chargement_data("data/deft09_appr_clean_fr.csv")

    X, vectorizer = vectorisation(texts)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    models = [
        MultinomialNB(alpha=0.01),
        LogisticRegression(C=10, max_iter=1000, n_jobs=-1, class_weight='balanced'),
        LinearSVC(class_weight='balanced', C=0.35)
    ]

    for model in models:
        evaluation(model, X_train, X_test, y_train, y_test, vectorizer)
