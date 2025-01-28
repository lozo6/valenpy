import digitalio
import busio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
srcs = None
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

# initialize display
display = Adafruit_SSD1680Z(122, 250,        # 2.13" HD mono display
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst,
    busy_pin=busy,
)

# rotating for landscape
display.rotation = 1

# transform image
def transform(image):
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = display.width / display.height
    if screen_ratio < image_ratio:
        scaled_width = image.width * display.height // image.height
        scaled_height = display.height
    else:
        scaled_width = display.width
        scaled_height = image.height * display.width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    x = scaled_width // 2 - display.width // 2
    y = scaled_height // 2 - display.height // 2
    image = image.crop((x, y, x + display.width, y + display.height)).convert("RGB")

    # Convert to Monochrome and Add dithering
    image = image.convert("1").convert("L")

    # return transformed image
    return image

if __name__ == "__main__":
    # load image
    image = Image.open("images/valentine.png")
    image = transform(image)

    # display image
    display.image(image)
    display.display()
