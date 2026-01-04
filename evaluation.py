from sklearn.metrics import classification_report, f1_score, accuracy_score


def chargement_predictions(fichier):
    """
    Charge le fichier avec les id et prédictions de partis associées
    """
    data = {}
    with open(fichier, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                raise ValueError(f"Ligne mal formée : {repr(line)}")
            doc_id, label = parts
            data[doc_id] = label
    return data


if __name__ == "__main__":
    # Paramètres
    predictions = "predictions.txt"
    reference = "deft09/Données de référence/deft09_parlement_ref_fr.txt"

    # Chargement
    pred = chargement_predictions(predictions)

    ref = chargement_predictions(reference)

    # Alignement
    y_true = []
    y_pred = []

    missing = 0
    for doc_id, true_label in ref.items():
        if doc_id in pred:
            y_true.append(true_label)
            y_pred.append(pred[doc_id])
        else:
            missing += 1

    if missing > 0:
        print(f"Il manque {missing} textes dans les predictions.")

    # Évaluation
    print("\nClassification report:")
    print(classification_report(y_true, y_pred, digits=3, zero_division=0))

    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Macro-F1:", f1_score(y_true, y_pred, average="macro"))
