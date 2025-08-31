// Récupérer la configuration depuis le backend
window.FrameConfig = {
    API_TOKEN: null
};

// Fonction pour récupérer le token depuis le backend
async function fetchApiToken() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        if (data.success && data.api_token) {
            window.FrameConfig.API_TOKEN = data.api_token;
        }
    } catch (error) {
        console.error('Erreur lors de la récupération du token API:', error);
    }
}

// Appeler la fonction pour récupérer le token au chargement de la page
fetchApiToken();

function toggleMode() {
    const body = document.querySelector('body');
    body.classList.toggle('dark-mode');
    const btn = document.querySelector('.toggle-mode-btn');
    btn.textContent = body.classList.contains('dark-mode') ? t('lightMode') : t('darkMode');
}