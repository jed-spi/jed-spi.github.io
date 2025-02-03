import os
import json
import requests
from bs4 import BeautifulSoup
import re

def download_page(url, filename):
    """Télécharge la page si elle n'existe pas localement."""
    if not os.path.exists(filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)
        else:
            raise Exception("Erreur lors du téléchargement de la page")


def get_laboratory(cv_link, UMR_dico):
    """Récupère le nom du laboratoire depuis la page CV."""
    response = requests.get(cv_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            UMR_id = int(soup.find("a", string=re.compile("UMR")).string[-4:])
            if UMR_id in UMR_dico:
                return UMR_dico[UMR_id]
            else:
                return "Inconnu DB " + str(UMR_id)
        except AttributeError:
            return "Inconnu"


def parse_page(filename, UMR_dico):
    """Parse le fichier HTML pour extraire les doctorants en 2ème année avec leur spécialité."""
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    data = []
    current_speciality = None  # Stocke la spécialité actuelle

    for element in soup.find_all(["h3", "li"]):  # On analyse chaque élément pertinent
        if element.name == "h3":
            current_speciality = element.text.strip()  # Mettre à jour la spécialité
        elif element.name == "li" and current_speciality:
            match = "1ère année" in element.text
            if match:
                author = element.find("a").text.strip().title()  # Extraire le nom
                cv_link = element.find("a")["href"]  # Lien vers le CV
                labo = get_laboratory(cv_link, UMR_dico)
                data.append({
                    "author": author,
                    "title": "title",
                    "session": None,  # Attribué plus tard
                    "id": None,  # Attribué plus tard
                    "labo": labo,
                    "speciality": current_speciality,  # Associer la spécialité
                    "cv": cv_link,  # Lien vers le CV
                    "abstract": None, # à la main
                    "poster": None  # à la main
                })
    return data

def assign_sessions_and_ids(filename, orateur):
    """Ouvre le JSON, supprime les orateurs, attribue sessions et IDs."""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    data = [entry for entry in data if entry["author"] not in orateur]

    specialities = {}
    for entry in data:
        specialities.setdefault(entry["speciality"], []).append(entry)

    for speciality, entries in specialities.items():
        half = len(entries) // 2
        for i, entry in enumerate(entries):
            entry["session"] = 1 if i < half else 2

    id_1, id_2 = 1, 1
    for entry in data:
        if entry["session"] == 1:
            entry["id"] = id_1
            id_1 += 1
        else:
            entry["id"] = id_2
            id_2 += 1

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    url = "https://doctorat.u-bordeaux.fr/aide/annuaires/annuaire-doctorantes-doctorants/load/5094"
    rawdata = "doctorants.html"
    filename = "doctorants.json"
    orateur = ["Marcel Dupont", "Fantine DeLaCroix"]
    UMR_dico = {
                5026: "IMCB",
                5031: "CRPP",
                5107: "CELIA",
                5218: "IMS",
                5319: "PASSAGES",
                5248: "CBMN",
                5295: "I2M",
                5298: "LP2N",
                5536: "CRMSB",
                5797: "LP2I",
                5798: "LOMA",
                5801: "LCTS",
                5804: "LAB"
            }

    download_page(url, rawdata)
    doctorants_data = parse_page(rawdata, UMR_dico)

    with open("doctorants.json", "w", encoding="utf-8") as json_file:
        json.dump(doctorants_data, json_file, ensure_ascii=False, indent=4)

    assign_sessions_and_ids(filename, orateur)
    print("Données extraites et enregistrées dans doctorants.json")

if __name__ == "__main__":
    main()
