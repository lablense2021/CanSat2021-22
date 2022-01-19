
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import threading 
import time

class oled():
    def __init__(self,log_function=print):
        
        self.oled_reset = digitalio.DigitalInOut(board.D4)
        self.WIDTH = 128
        self.HEIGHT = 32 
        self.update_time=0.25

        # Use for I2C.
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, i2c, addr=0x3c)
        # Clear display.
        self.oled.fill(0)
        self.oled.show()
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.log_function=log_function
        

    def start_scroll(self, text):
        self.stop_scroll()
        self.text_thread = threading.Thread(target=self.scroll_text, args=(str(text),))
        self.text_thread.start()

    def stop_scroll(self):
        self.scroll = False
        time.sleep(self.update_time+0.05)
        self.oled.fill(0)
        self.oled.show()

    
    def show_text(self, text):
        self.oled.fill(0)
        image = Image.new("1", (self.oled.width, self.oled.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Load default font.
        font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 20)

        (font_width, font_height) = font.getsize(text)
        draw.text(
        (0, self.oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255, 
        )
        self.oled.image(image)
        self.oled.show()
        


    def scroll_text(self, text):
        self.display_letters = 10
        self.ac_pos = 0
        text = text + "   "
        self.scroll= True
        self.oled.fill(0)
        self.oled.show()
        while self.scroll == True:
            self.show_text(text[self.ac_pos:self.ac_pos+self.display_letters])
            self.ac_pos = (self.ac_pos + 1)%len(text) #Problem bei Texten die nicht durch 3 teilbsr sind
            time.sleep(self.update_time)
        self.oled.fill(0)
        self.oled.show()


            
        




        

        

    





    

