import os
from PIL import Image, ImageEnhance

# Importation des modules EPD locaux
try:
    from . import epd7in3f
    from . import epdconfig
    EPD_AVAILABLE = True
    print("✅ Local EPD modules successfully imported")
except ImportError as e:
    epd7in3f = None
    epdconfig = None
    EPD_AVAILABLE = False
    print(f"❌ Local EPD modules not available: {e}")

# Definition of the display() command
def display():
    print(f"=== Starting display function ===")
    print(f"EPD modules available: {EPD_AVAILABLE}")
    
    # Si les modules EPD ne sont pas disponibles, on affiche un message et on retourne True
    if not EPD_AVAILABLE:
        print("⚠️  EPD modules not available, skipping display")
        return True
    
    try:
        print("Creating EPD object...")
        # Initialize the screen
        epd = epd7in3f.EPD()
        print("✅ EPD object created")
        
        print("Initializing EPD...")
        epd.init()
        print("✅ EPD initialized")
        
        print("Clearing screen...")
        epd.Clear()
        print("✅ Screen cleared")
        
        # Open the picture - chemin corrigé
        image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'OnWeb', 'img.png')
        print(f"Looking for image at: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return False
            
        print("Loading image...")
        # Charger l'image en suivant l'approche du script de test
        image = Image.open(image_path)
        print("✅ Image loaded")
        
        # Afficher l'image en utilisant la méthode getbuffer du script officiel
        print("Converting image with official method...")
        image_buffer = epd.getbuffer(image)
        print("✅ Image converted")
        
        # Displays the image
        print("Displaying image...")
        epd.display(image_buffer)
        print("✅ Image displayed")
        
        # Puts the screen in sleep mode
        print("Putting EPD to sleep...")
        epd.sleep()
        print("✅ EPD in sleep mode")
        return True
    except Exception as e:
        print(f"❌ Error during display: {e}")
        import traceback
        traceback.print_exc()
        return False

