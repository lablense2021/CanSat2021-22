
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import threading 

class oled():
    def __init__(self,log_function=print):
        
        self.oled_reset = digitalio.DigitalInOut(board.D4)
        self.WIDTH = 128
        self.HEIGHT = 32 
       

        # Use for I2C.
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, i2c, addr=0x3c)
        # Clear display.
        
        self.oled.show()
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.log_function=log_function
        

    def start_scroll(self, text):
        self.scroll= False
        self.scroll= True
        text_thread = threading.Thread(target=self.scroll_text(text))
        text.thread.start()

    def stop_scroll(self):
        self.scroll= False

    
    def show_text(self, text):
        self.oled.fill(0)
        self.oled.display.text(text, 0, 0, 1)
        self.oled.show()


    def scroll_text(self, text):
        self.display_letters = 5
        self.ac_pos = 0
        while self.scroll== True:
            self.show_text(text[self.ac_pos:self.ac_pos+self.display_letters])
            self.ac_pos = (self.ac_pos + 1)%len(text)


            
        




        

        

    





    

