window.translations = {
  en: {
    home: 'Home',
    tags: 'Tag Authorized',
    bantags: 'Forbidden Tag',
    darkMode: 'Dark Mode',
    lightMode: 'Light Mode',
    frameAdmin: 'Frame Admin 🖼️',
    uploadImage: 'Upload image',
    updateImage: "Update Image",
    selectFunction: 'Select the function to perform :',
    updateFunction: 'Update function',
    updateFrame: 'Update The Frame',
    returnHome: 'Return Home',
    tableAllowed: 'Table of allowed tags',
    tableProhibited: 'Table of prohibited tags',
    addNewWord: 'Add a new word:',
    add: 'Add',
    word: 'Word',
    action: 'Action',
    delete: 'Delete',
    enterWord: 'Please enter a word to add.',
    alreadyThere: 'This word is already in the list.',
    functionUpdated: 'Function Updated',
    frameUpdating: 'The Frame is being updated !'
  },
  fr: {
    home: 'Accueil',
    tags: 'Tags autorisés',
    bantags: 'Tags interdits',
    darkMode: 'Mode sombre',
    lightMode: 'Mode clair',
    frameAdmin: 'Administration du cadre 🖼️',
    uploadImage: 'Téléverser une image',
    updateImage: "Mettre à jour l'image",
    selectFunction: 'Choisir la fonction :',
    updateFunction: 'Mettre à jour la fonction',
    updateFrame: 'Mettre à jour le cadre',
    returnHome: 'Retour accueil',
    tableAllowed: 'Table des tags autorisés',
    tableProhibited: 'Table des tags interdits',
    addNewWord: 'Ajouter un nouveau mot :',
    add: 'Ajouter',
    word: 'Mot',
    action: 'Action',
    delete: 'Supprimer',
    enterWord: 'Veuillez entrer un mot à ajouter.',
    alreadyThere: 'Ce mot est déjà dans la liste.',
    functionUpdated: 'Fonction mise à jour',
    frameUpdating: 'Le cadre est en cours de mise à jour !'
  }
};

window.language = navigator.language.startsWith('fr') ? 'fr' : 'en';
window.t = (key) => window.translations[window.language][key] || key;

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const text = t(key);
    if (el.tagName === 'INPUT' && el.type !== 'file') {
      if (el.placeholder) {
        el.placeholder = text;
      } else {
        el.value = text;
      }
    } else {
      el.textContent = text;
    }
  });
});
