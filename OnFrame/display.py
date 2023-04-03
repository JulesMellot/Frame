import os
from PIL import Image, ImageEnhance
from waveshare_epd.epd7in3f import EPD

#Definition of the display() command
def display():
    # Initialize the screen
    epd = EPD()
    epd.init()
    print("INIT DONE")
    epd.Clear()
    print("SCREEN HAS BEEN CLEAN")
    # Open the picture
    image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img.png'))
    print("IMG LOADED")
    # Rotates the image 90 degrees clockwise
    image = image.rotate(270, expand=True)
    print("IMG ROTATED")
    # Create an ImageEnhance.Color object
    converter_color = ImageEnhance.Color(image)
    converter_bri = ImageEnhance.Brightness(image)
    # Increase saturation by 210%, if you don't like this settings you can change as you want :)
    image = converter_color.enhance(2.1)
    print("COLOR AT 210%")
    # Increase brightness by 130%, if you don't like this settings you can change as you want :)
    image = converter_bri.enhance(1.3)
    print("BRIGHTNESS AT 130%")
    # Resizes the image to fit the screen size
    image = image.resize((800, 480))
    # Converts image to screen color mode
    image = image.convert('RGB')
    # Displays the image
    epd.display(epd.getbuffer(image))
    print("IMG DISPLAY")
    # Puts the screen in sleep mode
    epd.sleep()
    return True
