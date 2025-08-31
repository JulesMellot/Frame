// Le token API est maintenant récupéré dynamiquement depuis client-config.js
// Cette variable sera définie dans client-config.js
let API_TOKEN = null;

function toggleMode() {
    const body = document.querySelector('body');
    body.classList.toggle('dark-mode');
    const btn = document.querySelector('.toggle-mode-btn');
    btn.textContent = body.classList.contains('dark-mode') ? t('lightMode') : t('darkMode');
}
  
