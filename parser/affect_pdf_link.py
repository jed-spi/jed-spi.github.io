import json
import requests

json_path = "data/poster.json"

base_url = "https://jed-spi.github.io/data/2025/"
cv_prefix = "CV_"
abstract_prefix = "ABSTRACT_"

def make_key(author):
    parts = author.strip().split()
    if len(parts) < 2:
        raise ValueError(f"Nom d'auteur invalide : '{author}'")
    prenom = parts[0].upper()
    nom = "-".join(part.upper() for part in parts[1:])
    return f"{prenom}_{nom}"

def url_exists(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    author = entry.get("author", "").strip()
    try:
        key = make_key(author)
    except ValueError as e:
        print(f"[Erreur] {e}")
        continue

    cv_url = f"{base_url}{cv_prefix}{key}.pdf"
    abstract_url = f"{base_url}{abstract_prefix}{key}.pdf"

    # Vérification
    if url_exists(cv_url):
        entry["cv"] = cv_url
    else:
        entry["cv"] = None
        print(f"[CV manquant] {author} → {cv_url}")

    if url_exists(abstract_url):
        entry["abstract"] = abstract_url
    else:
        entry["abstract"] = None
        print(f"[Abstract manquant] {author} → {abstract_url}")

# Écriture du JSON mis à jour
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Mise à jour terminée.")
