async function load(file, elementId) {
  try {
    const response = await fetch(file);  // Charger le fichier HTML
    const data = await response.text();  // Résoudre la promesse en texte
    document.getElementById(elementId).innerHTML = data;  // Insérer le contenu dans la balise cible
  } catch (error) {
    console.error('Erreur lors du chargement du fichier:', error);
  }
}

// Appel de la fonction pour charger le header et le footer
load('https://jed-spi.github.io/includes/header.html', 'header');
load('https://jed-spi.github.io/includes/footer.html', 'footer');
