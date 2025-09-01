const translations = {
  en: {
    home: "Home",
    tags: "Tag Authorized",
    bantags: "Forbidden Tag",
    apiToken: "API Token",
    calibration: "Calibration",
    frameAdmin: "Frame Admin 🖼️",
    uploadImage: "Upload image",
    updateImage: "Update Image",
    selectFunction: "Select the function to perform :",
    updateFunction: "Update function",
    updateFrame: "Update The Frame",
    darkMode: "Dark Mode",
    lightMode: "Light Mode",
    frameUpdating: "The frame is updating...",
    functionUpdated: "Function updated",
    calibrateScreen: "Calibrate Screen",
    calibrationStarted: "Calibration started. Check your e-Paper display.",
    calibrationFailed: "Calibration failed",
    // Calibration page translations
    calibrationInstructions: "Calibration Instructions",
    calibrationExplanation: "This procedure will help you check and correct the orientation of your e-Paper screen. A special image will be displayed with visual markers in each corner.",
    expectedOrientation: "Expected orientation:",
    topLeft: "Top left",
    topRight: "Top right",
    bottomLeft: "Bottom left",
    bottomRight: "Bottom right",
    startCalibration: "Start Calibration",
    calibrationResult: "Calibration Result",
    checkDisplay: "Check your e-Paper display. The calibration image should be displayed.",
    adjustOrientation: "Adjust Orientation",
    orientationExplanation: "If the orientation is not correct, you can adjust the settings in the source code. Modify the file frame/epd7in3f.py and change the rotation value."
  },
  fr: {
    home: "Accueil",
    tags: "Tag Autorisé",
    bantags: "Tag Interdit",
    apiToken: "Token API",
    calibration: "Calibration",
    frameAdmin: "Admin du Cadre 🖼️",
    uploadImage: "Uploader une image",
    updateImage: "Mettre à jour l'image",
    selectFunction: "Sélectionnez la fonction à effectuer :",
    updateFunction: "Mettre à jour la fonction",
    updateFrame: "Mettre à jour le cadre",
    darkMode: "Mode Sombre",
    lightMode: "Mode Clair",
    frameUpdating: "Le cadre se met à jour...",
    functionUpdated: "Fonction mise à jour",
    calibrateScreen: "Calibrer l'écran",
    calibrationStarted: "Calibration démarrée. Vérifiez votre écran e-Paper.",
    calibrationFailed: "Échec de la calibration",
    // Calibration page translations
    calibrationInstructions: "Instructions de calibration",
    calibrationExplanation: "Cette procédure va vous aider à vérifier et corriger l'orientation de votre écran e-Paper. Une image spéciale va être affichée avec des repères visuels dans chaque coin.",
    expectedOrientation: "Orientation attendue :",
    topLeft: "Haut gauche",
    topRight: "Haut droite",
    bottomLeft: "Bas gauche",
    bottomRight: "Bas droite",
    startCalibration: "Démarrer la calibration",
    calibrationResult: "Résultat de la calibration",
    checkDisplay: "Vérifiez votre écran e-Paper. L'image de calibration devrait s'afficher.",
    adjustOrientation: "Ajuster l'orientation",
    orientationExplanation: "Si l'orientation n'est pas correcte, vous pouvez ajuster les paramètres dans le code source. Modifiez le fichier frame/epd7in3f.py et changez la valeur de rotation."
  }
};

function t(key) {
  const lang = localStorage.getItem('language') || 'en';
  return translations[lang][key] || key;
}

function setLanguage(lang) {
  localStorage.setItem('language', lang);
  location.reload();
}

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
