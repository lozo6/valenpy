import time
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
display = Adafruit_SSD1680Z(122, 250,
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst,
    busy_pin=busy,
)

# initialize buttons
up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input(pull=digitalio.Pull.UP)
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input(pull=digitalio.Pull.UP)

# rotating for landscape
display.rotation = 1

# List of images to display
images = ["images/1.png", "images/2.png"]
current_image_index = 0

# Function to transform image
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
    image = image.crop((x, y, x + display.width, y + display.height)).convert("L")

    # Convert to Monochrome and Add dithering
    image = image.convert("1", dither=Image.FLOYDSTEINBERG)

    # Return transformed image
    return image

# Function to display an image
def display_image(image_path):
    image = Image.open(image_path)
    transformed_image = transform(image)
    display.image(transformed_image)
    display.display()

def main():
    global current_image_index

    # Display the initial image
    display_image(images[current_image_index])

    while True:
        # Check if the up button is pressed
        if not up_button.value:
            print("Up Button Pushed")
            current_image_index = (current_image_index + 1) % len(images)  # Cycle forward
            display_image(images[current_image_index])
            time.sleep(0.2)

        # Check if the down button is pressed
        if not down_button.value:
            print("Down Button Pushed")
            current_image_index = (current_image_index - 1) % len(images)  # Cycle backward
            display_image(images[current_image_index])
            time.sleep(0.2)

if __name__ == "__main__":
    main()
