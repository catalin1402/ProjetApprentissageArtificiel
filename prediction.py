import pandas as pd
import joblib


def chargement_test(fichier_test):
    """
    Chargement du corpus de test.
    """
    df = pd.read_csv(fichier_test)
    return df["id"].tolist(), df["text"].tolist()


if __name__ == "__main__":
    # Paramètres
    chemin_test = "data/deft09_test_clean_fr.csv"
    modele = "model_linearsvc.joblib"
    vectorisation = "vectorizer_linearsvc.joblib"
    sortie = "predictions.txt"

    # Chargement
    ids, texts = chargement_test(chemin_test)

    model = joblib.load(modele)
    vectorizer = joblib.load(vectorisation)

    # Vectorisation
    X_test = vectorizer.transform(texts)

    # Prédiction
    y_pred = model.predict(X_test)

    # Sauvegarde
    with open(sortie, "w", encoding="utf-8") as f:
        for doc_id, label in zip(ids, y_pred):
            f.write(f"{doc_id}\t{label}\n")
