// ======================
// 🎟️ FILE D’ATTENTE
// ======================

// Position initiale aléatoire
const positionInitiale = Math.floor(Math.random() * 500) + 100;
let positionActuelle = positionInitiale;
let progress = 0;

const categories = [
    "Cat Or",
    "Cat 1",
    "Cat 2",
    "Cat 3",
    "Fosse",
    "Fosse Or"
  ];
  
  // Choisir 2 catégories à marquer comme épuisées
  const shuffled = categories.sort(() => 0.5 - Math.random());
  const outOfStock = shuffled.slice(0, 2);
  
  const container = document.getElementById("categories-container");
  
  categories.forEach(name => {
    const isDisabled = outOfStock.includes(name);
    const safeId = name.toLowerCase().replace(/\s+/g, "-");
  
    const wrapper = document.createElement("div");
    wrapper.className = "category";
    wrapper.id = `cat-${safeId}`;  
  
    const header = document.createElement("div");
    header.className = "header";
    header.innerHTML = `
      <span>${name}</span>
      <span class="toggle">➤</span>
    `;
  
    const content = document.createElement("div");
    content.className = "content";
    content.innerHTML = `
      <label>${name}</label><br>
      <button class="moins">-</button>
      <span class="quantite">0</span>
      <button class="plus">+</button>
    `;
  
    if (isDisabled) {
      wrapper.classList.add("disabled");
      content.innerHTML += `<p style="color: red;">Catégorie épuisée</p>`;
    }
  
    header.addEventListener("click", () => {
      const currentlyVisible = content.style.display === "block";
      content.style.display = currentlyVisible ? "none" : "block";
      header.querySelector(".toggle").textContent = currentlyVisible ? "➤" : "▼";
    });
  
    wrapper.appendChild(header);
    wrapper.appendChild(content);
    container.appendChild(wrapper);
  
    if (!isDisabled) {
      const plus = content.querySelector(".plus");
      const moins = content.querySelector(".moins");
      const quantite = content.querySelector(".quantite");
  
      plus.addEventListener("click", () => {
        let q = parseInt(quantite.textContent);
        if (q < 8) quantite.textContent = q + 1;
      });
  
      moins.addEventListener("click", () => {
        let q = parseInt(quantite.textContent);
        if (q > 0) quantite.textContent = q - 1;
      });
    }
  });  
  

// Affichage initial
document.getElementById("position-file").textContent =
  `Vous êtes n°${positionActuelle} dans la file d’attente...`;

// Lancer la barre de progression
const interval = setInterval(() => {
  progress += 2;
  document.getElementById("progression").style.width = `${progress}%`;

  // Calcul dynamique de la position
  const positionsRestantes = Math.floor(positionInitiale * (1 - progress / 100));
  positionActuelle = Math.max(1, positionsRestantes);
  document.getElementById("position-file").textContent =
    `Vous êtes n°${positionActuelle} dans la file d’attente...`;

  // Fin de la file
  if (progress >= 100) {
    clearInterval(interval);

    // Masquer la barre
    document.getElementById("barre-progression").style.display = "none";

    // Remplacer le message par une attente finale
    const messageContainer = document.getElementById("position-file");
    messageContainer.textContent = "Vous allez être redirigé...";

    // Ajouter un spinner
    const spinner = document.createElement("div");
    spinner.className = "spinner";
    messageContainer.insertAdjacentElement('afterend', spinner);

    // Délai aléatoire entre 2 et 6 secondes avant apparition du bouton
    const delai = Math.floor(Math.random() * 4000) + 2000;
    setTimeout(() => {
      document.getElementById("file-attente").style.display = "none";
      document.getElementById("acheter").style.display = "inline-block";
    }, delai);
  }
}, 100);


// ======================
// 🛒 CLIC SUR "ACHETER MAINTENANT"
// ======================

document.getElementById('acheter').addEventListener('click', () => {
    document.getElementById('acheter').style.display = 'none';
    document.getElementById('loader').style.display = 'block';
  
    // Simulation court chargement
    setTimeout(() => {
      document.getElementById('loader').style.display = 'none';
      document.getElementById('formulaire').style.display = 'block';
    }, 1000);
  });

  
  // ======================
// ✅ SOUMISSION DU FORMULAIRE
// ======================

document.getElementById('formulaire').addEventListener('submit', function (e) {
    e.preventDefault();
  
    // Récupération des champs
    const cb = document.querySelector('[name="cb"]').value.trim();
    const exp = document.querySelector('[name="expiration"]').value.trim();
    const cvv = document.querySelector('[name="cvv"]').value.trim();
  
    // Validations
    const cbValide = cb.length === 16 && /^\d+$/.test(cb);
    const cvvValide = cvv.length === 3 && /^\d+$/.test(cvv);
    const expValide = exp !== "";
  
    if (!cbValide || !cvvValide || !expValide) {
      document.getElementById('erreur').style.display = 'block';
      return;
    }
  
    // Succès
    document.getElementById('erreur').style.display = 'none';
    document.getElementById('formulaire').style.display = 'none';
    document.getElementById('confirmation').style.display = 'block';

  });
  
  