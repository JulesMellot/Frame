# *****************************************************************************
# * | File        :	  epd7in3f.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2022-10-20
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
from . import epdconfig

import PIL
from PIL import Image
import io

# Display resolution
EPD_WIDTH       = 800
EPD_HEIGHT      = 480

logger = logging.getLogger(__name__)

class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.BLACK  = 0x000000   #   0000  BGR
        self.WHITE  = 0xffffff   #   0001
        self.GREEN  = 0x00ff00   #   0010
        self.BLUE   = 0xff0000   #   0011
        self.RED    = 0x0000ff   #   0100
        self.YELLOW = 0x00ffff   #   0101
        self.ORANGE = 0x0080ff   #   0110
        
    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(20) 
        epdconfig.digital_write(self.reset_pin, 0)         # module reset
        epdconfig.delay_ms(2)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(20)   

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)
        
    # send a lot of data   
    def send_data2(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte2(data)
        epdconfig.digital_write(self.cs_pin, 1)
        
    def ReadBusyH(self):
        logger.debug("e-Paper busy H")
        while(epdconfig.digital_read(self.busy_pin) == 0):      # 0: busy, 1: idle
            epdconfig.delay_ms(5)
        logger.debug("e-Paper busy H release")

    def TurnOnDisplay(self):
        self.send_command(0x04) # POWER_ON
        self.ReadBusyH()

        self.send_command(0x12) # DISPLAY_REFRESH
        self.send_data(0X00)
        self.ReadBusyH()
        
        self.send_command(0x02) # POWER_OFF
        self.send_data(0X00)
        self.ReadBusyH()
        
    def init(self):
        if (epdconfig.module_init() != 0):
            return -1
        # EPD hardware init start
        self.reset()
        self.ReadBusyH()
        epdconfig.delay_ms(30)

        self.send_command(0xAA)    # CMDH
        self.send_data(0x49)
        self.send_data(0x55)
        self.send_data(0x20)
        self.send_data(0x08)
        self.send_data(0x09)
        self.send_data(0x18)

        self.send_command(0x01)
        self.send_data(0x3F)
        self.send_data(0x00)
        self.send_data(0x32)
        self.send_data(0x2A)
        self.send_data(0x0E)
        self.send_data(0x2A)

        self.send_command(0x00)
        self.send_data(0x5F)
        self.send_data(0x69)

        self.send_command(0x03)
        self.send_data(0x00)
        self.send_data(0x54)
        self.send_data(0x00)
        self.send_data(0x44) 

        self.send_command(0x05)
        self.send_data(0x40)
        self.send_data(0x1F)
        self.send_data(0x1F)
        self.send_data(0x2C)

        self.send_command(0x06)
        self.send_data(0x6F)
        self.send_data(0x1F)
        self.send_data(0x1F)
        self.send_data(0x22)

        self.send_command(0x08)
        self.send_data(0x6F)
        self.send_data(0x1F)
        self.send_data(0x1F)
        self.send_data(0x22)

        self.send_command(0x13)    # IPC
        self.send_data(0x00)
        self.send_data(0x04)

        self.send_command(0x30)
        self.send_data(0x3C)

        self.send_command(0x41)     # TSE
        self.send_data(0x00)

        self.send_command(0x50)
        self.send_data(0x3F)

        self.send_command(0x60)
        self.send_data(0x02)
        self.send_data(0x00)

        self.send_command(0x61)
        self.send_data(0x03)
        self.send_data(0x20)
        self.send_data(0x01) 
        self.send_data(0xE0)

        self.send_command(0x82)
        self.send_data(0x1E) 

        self.send_command(0x84)
        self.send_data(0x00)

        self.send_command(0x86)    # AGID
        self.send_data(0x00)

        self.send_command(0xE3)
        self.send_data(0x2F)

        self.send_command(0xE0)   # CCSET
        self.send_data(0x00) 

        self.send_command(0xE6)   # TSSET
        self.send_data(0x00)
        return 0

    def getbuffer(self, image):
        # Create a pallette with the 7 colors supported by the panel
        # According to Waveshare documentation:
        # Black: 0b0000 (0x0)
        # White: 0b0001 (0x1)
        # Green: 0b0010 (0x2)
        # Blue: 0b0011 (0x3)
        # Red: 0b0100 (0x4)
        # Yellow: 0b0101 (0x5)
        # Orange: 0b0110 (0x6)
        pal_image = Image.new("P", (1,1))
        pal_image.putpalette( (0,0,0,  255,255,255,  0,255,0,   0,0,255,  255,0,0,  255,255,0, 255,128,0) + (0,0,0)*249)

        # Check if we need to rotate the image
        imwidth, imheight = image.size
        print(f"Original image dimensions: {imwidth}x{imheight}")
        print(f"Screen dimensions: {self.width}x{self.height}")
        
        # Always resize to screen dimensions first
        if imwidth != self.width or imheight != self.height:
            print(f"Resizing image from {imwidth}x{imheight} to {self.width}x{self.height}")
            image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
            imwidth, imheight = self.width, self.height

        # Apply color enhancement before quantization
        from PIL import ImageEnhance
        # Increase saturation and brightness for better color display
        converter_color = ImageEnhance.Color(image)
        converter_bri = ImageEnhance.Brightness(image)
        converter_con = ImageEnhance.Contrast(image)
        
        image = converter_color.enhance(2.1)   # Increase saturation for vivid colors
        image = converter_bri.enhance(1.3)    # Increase brightness for better visibility
        image = converter_con.enhance(1.2)    # Increase contrast for sharper image

        # Check rotation setting from file or use default (0)
        rotation = self.get_rotation_setting()
        print(f"Applying rotation: {rotation} degrees")
        
        if rotation != 0:
            image = image.rotate(rotation, expand=True)

        image_temp = image

        # Convert the source image to the 7 colors with dithering
        # Using Floyd-Steinberg dithering as recommended by Waveshare
        image_7color = image_temp.convert("RGB").quantize(
            palette=pal_image, 
            dither=Image.Dither.FLOYDSTEINBERG
        )
        buf_7color = bytearray(image_7color.tobytes('raw'))

        # Pack 4-bit color values into bytes
        # Two pixels per byte as per Waveshare specification
        buf = [0x00] * int(self.width * self.height / 2)
        idx = 0
        for i in range(0, len(buf_7color), 2):
            buf[idx] = (buf_7color[i] << 4) + buf_7color[i+1]
            idx += 1
            
        return buf

    def display(self, image):
        self.send_command(0x10)
        self.send_data2(image)

        self.TurnOnDisplay()
        
    def Clear(self, color=0x11):
        self.send_command(0x10)
        self.send_data2([color] * int(self.height) * int(self.width/2))

        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0XA5)
        
        epdconfig.delay_ms(2000)
        epdconfig.module_exit()
        
    def get_rotation_setting(self):
        """Get rotation setting from configuration file or return default (0)"""
        import os
        import json
        
        config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'OnWeb', 'rotation.json')
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('rotation', 0)
            else:
                # Create default configuration
                default_config = {'rotation': 0}
                os.makedirs(os.path.dirname(config_file), exist_ok=True)
                with open(config_file, 'w') as f:
                    json.dump(default_config, f)
                return 0
        except Exception as e:
            print(f"Error reading rotation setting: {e}")
            return 0
            
### END OF FILE ###

