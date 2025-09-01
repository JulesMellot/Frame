from PIL import Image, ImageDraw, ImageFont
import os

def create_calibration_image(width=800, height=480):
    """Crée une image de calibration pour vérifier l'orientation"""
    
    # Créer une image avec des repères visuels
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Dessiner des carrés colorés dans chaque coin pour l'identification
    square_size = 50
    
    # Coin supérieur gauche - Noir
    draw.rectangle([0, 0, square_size, square_size], fill='black')
    
    # Coin supérieur droit - Rouge
    draw.rectangle([width-square_size, 0, width, square_size], fill='red')
    
    # Coin inférieur gauche - Bleu
    draw.rectangle([0, height-square_size, square_size, height], fill='blue')
    
    # Coin inférieur droit - Vert
    draw.rectangle([width-square_size, height-square_size, width, height], fill='green')
    
    # Ajouter du texte explicatif
    try:
        # Essayer d'utiliser une police système
        font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
        font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
    except:
        # Utiliser la police par défaut si la police système n'est pas disponible
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Texte central d'explication
    text = "CALIBRATION"
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill='black', font=font_large)
    
    # Instructions
    instructions = [
        "Vérifiez l'orientation de l'écran :",
        "• Le carré NOIR doit être en HAUT À GAUCHE",
        "• Le carré ROUGE doit être en HAUT À DROITE",
        "• Le carré BLEU doit être en BAS À GAUCHE",
        "• Le carré VERT doit être en BAS À DROITE"
    ]
    
    y_offset = y + 60
    for instruction in instructions:
        bbox = draw.textbbox((0, 0), instruction, font=font_medium)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_offset), instruction, fill='black', font=font_medium)
        y_offset += 35
    
    # Numéros dans les coins
    draw.text((10, 10), "1", fill='white', font=font_large)
    draw.text((width-30, 10), "2", fill='white', font=font_large)
    draw.text((10, height-40), "3", fill='white', font=font_large)
    draw.text((width-30, height-40), "4", fill='white', font=font_large)
    
    return image

def test_orientation():
    """Teste l'orientation actuelle de l'écran"""
    print("Creating calibration image...")
    image = create_calibration_image()
    
    # Sauvegarder l'image de calibration
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    web_dir = os.path.join(base_dir, 'OnWeb')
    image_path = os.path.join(web_dir, 'calibration.png')
    
    # S'assurer que le répertoire existe
    os.makedirs(web_dir, exist_ok=True)
    
    image.save(image_path)
    print(f"Calibration image saved to {image_path}")
    
    return image

if __name__ == "__main__":
    test_orientation()