export function loadPosterSession(url_data, session) {
    // Charger le fichier JSON et générer le contenu de la session poster
    fetch(url_data)
        .then(response => response.json())
        .then(data => {
            const sessionDiv = document.getElementById('poster-session');

            // Vérifier que l'élément existe
            if (!sessionDiv) {
                console.error('Erreur : Élément avec ID "poster-session" introuvable.');
                return;
            }

            // Trier les posters
            const sortedPosters = data
                .filter(poster => poster.session === session) // Conserver uniquement la session spécifiée
                .sort((a, b) => a.id - b.id); // Trier par id

            // Création de la liste des posters
            const ul = document.createElement('ul');
            sortedPosters.forEach((poster) => {
                if (poster.title != "title") {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <strong>${poster.id} :</strong> ${poster.title} <br>
                        <em>Auteur : </em>${poster.author} en ${poster.speciality} au laboratoire ${poster.labo} <br>
                        ${poster.cv ? `<a href="${poster.cv}">[CV]</a>` : ''}
                        ${poster.abstract ? `<a href="${poster.abstract}">[abstract]</a>` : ''}
                        ${poster.poster ? `<a href="${poster.poster}">[poster]</a>` : ''}
                    `;
                    ul.appendChild(li);
                }
            });

            sessionDiv.appendChild(ul);
        })
        .catch(error =>
            console.error('Erreur lors du chargement du programme de la session posters :', error)
        );
}
