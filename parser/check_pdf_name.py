import os

def collect_and_compare_files(folder_path):
    cv_list = []
    abstract_list = []

    # Parcours des fichiers dans le dossier
    for filename in os.listdir(folder_path):
        if filename.startswith("CV"):
            name = filename[len("CV"):].strip()
            cv_list.append(name)
        elif filename.startswith("ABSTRACT"):
            name = filename[len("ABSTRACT"):].strip()
            abstract_list.append(name)

    # Conversion en ensembles pour comparaison
    cv_set = set(cv_list)
    abstract_set = set(abstract_list)

    only_in_cv = cv_set - abstract_set
    only_in_abstract = abstract_set - cv_set

    print("Fichiers uniquement dans CV :")
    for item in sorted(only_in_cv):
        print(f"  {item}")

    print("\nFichiers uniquement dans ABSTRACT :")
    for item in sorted(only_in_abstract):
        print(f"  {item}")

# Exemple d'utilisation
if __name__ == "__main__":
    dossier = "../data/2025"
    collect_and_compare_files(dossier)
