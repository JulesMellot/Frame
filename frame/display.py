import os
from PIL import Image, ImageEnhance

# Importation conditionnelle du module EPD
try:
    from waveshare_epd import epd7in3f
    EPD_AVAILABLE = True
    print("✅ EPD module successfully imported")
except ImportError as e:
    epd7in3f = None
    EPD_AVAILABLE = False
    print(f"❌ EPD module not available: {e}")

#Definition of the display() command
def display():
    print(f"=== Starting display function ===")
    print(f"EPD module available: {EPD_AVAILABLE}")
    
    # Si le module EPD n'est pas disponible, on affiche un message et on retourne True
    if not EPD_AVAILABLE:
        print("⚠️  EPD module not available, skipping display")
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
        
        # Open the picture
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img.png')
        image_path = image_path.replace('/frame', '/OnWeb')  # Ajuster le chemin
        print(f"Looking for image at: {image_path}")
        
        if not os.path.exists(image_path):
            # Essayer le chemin direct
            image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'OnWeb', 'img.png')
            print(f"Trying alternative path: {image_path}")
            
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return False
            
        print("Loading image...")
        image = Image.open(image_path)
        print("✅ Image loaded")
        
        # Rotates the image 90 degrees clockwise
        print("Rotating image...")
        image = image.rotate(270, expand=True)
        print("✅ Image rotated")
        
        # Create an ImageEnhance.Color object
        print("Enhancing colors...")
        converter_color = ImageEnhance.Color(image)
        converter_bri = ImageEnhance.Brightness(image)
        
        # Increase saturation by 210%, if you don't like this settings you can change as you want :)
        image = converter_color.enhance(2.1)
        print("✅ Color enhanced")
        
        # Increase brightness by 130%, if you don't like this settings you can change as you want :)
        image = converter_bri.enhance(1.3)
        print("✅ Brightness enhanced")
        
        # Resizes the image to fit the screen size
        print("Resizing image...")
        image = image.resize((800, 480))
        print("✅ Image resized")
        
        # Converts image to screen color mode
        print("Converting image mode...")
        image = image.convert('RGB')
        print("✅ Image mode converted")
        
        # Displays the image
        print("Displaying image...")
        epd.display(epd.getbuffer(image))
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

