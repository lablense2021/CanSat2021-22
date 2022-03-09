
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import threading 
import time
import functions

class oled():
    def __init__(self,log_function=print):
        
        self.oled_reset = digitalio.DigitalInOut(board.D4)
        self.WIDTH = 128
        self.HEIGHT = 32 
        self.update_time=0.5

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
        try:
            while self.text_thread.is_alive():
                time.sleep(0.1)
        except:
            self.log_function("no text_thread to stop found")
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
        hops=2
        text = text + (len(text)%hops)*" "
        self.scroll= True
        self.oled.fill(0)
        self.oled.show()
        self.show_text(text[self.ac_pos:self.ac_pos+self.display_letters])
        last_time=functions.cut_time(time.time())
        while self.scroll == True:
            if functions.cut_time(time.time())-last_time >= self.update_time:
                self.ac_pos = (self.ac_pos + hops )%len(text) #Problem bei Texten die nicht durch 3 teilbsr sind
                self.show_text(text[self.ac_pos:self.ac_pos+self.display_letters])
                last_time=functions.cut_time(time.time())
            time.sleep(0.1)
        self.oled.fill(0)
        self.oled.show()


    def close_oled(self):
        self.oled.fill(0)
        self.stop_scroll()


            
        




        

        

    





    

