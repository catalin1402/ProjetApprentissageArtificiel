import xml.etree.ElementTree as ET
import re
import csv
from pathlib import Path


def normalisation(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def nettoyage(text):
    # suppression des balises
    text = re.sub(r"<[^>]+>", " ", text)
    # on conserve les lettres, chiffres, accents
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chargement_fichier(chemin_entree):
    tree = ET.parse(chemin_entree)
    root = tree.getroot()

    data = []

    for doc in root.findall("doc"):
        # id
        doc_id = doc.attrib.get("id")

        # texte
        paragraphes = doc.findall(".//texte/p")
        raw_text = " ".join(p.text or "" for p in paragraphes)

        text = normalisation(raw_text)
        text = nettoyage(text)

        if text:
            data.append((doc_id, text))

    return data


def sauvegarde_csv(data, chemin_sortie):
    with open(chemin_sortie, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text"])
        for doc_id, text in data:
            writer.writerow([doc_id, text])


if __name__ == "__main__":
    input_xml = Path("deft09/Corpus de test/deft09_parlement_test_fr.xml")
    output_csv = Path("data/deft09_test_clean_fr.csv")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    data = chargement_fichier(input_xml)
    sauvegarde_csv(data, output_csv)

