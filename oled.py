
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class oled():
    def __init__(self):
        # Define the Reset Pin
        oled_reset = digitalio.DigitalInOut(board.D4)
        # Change these
        # to the right size for your display!
        WIDTH = 128
        HEIGHT = 64  # Change to 64 if needed
        BORDER = 5

        # Use for I2C.
        i2c = board.I2C()
        oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3d, reset=oled_reset)

        # Clear display.
        oled.fill(0)
        oled.show()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (oled.width, oled.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Load default font.
        font = ImageFont.load_default()

    
    #def startup():
