// Récupérer la configuration depuis le backend
window.FrameConfig = {
    API_TOKEN: null
};

// Fonction pour récupérer le token depuis le backend
async function fetchApiToken() {
    try {
        const response = await fetch('/api/config');
        if (!response.ok) {
            console.error('Erreur HTTP lors de la récupération du token API:', response.status);
            return;
        }
        const data = await response.json();
        if (data.success && data.api_token) {
            window.FrameConfig.API_TOKEN = data.api_token;
            console.log('Token API récupéré avec succès');
        } else {
            console.warn('Token API non disponible dans la réponse');
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