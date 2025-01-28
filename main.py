import digitalio
import busio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
srcs = None

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
up_button = digitalio.DigitalInOut(board.D6)
up_button.switch_to_input()
down_button = digitalio.DigitalInOut(board.D5)
down_button.switch_to_input()

# rotating for landscape
display.rotation = 1

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
    # image = image.convert("1").convert("L")

    # Return transformed image
    return image

# Function to display an image
def display_image(image_path):
    image = Image.open(image_path)
    transformed_image = transform(image)
    display.image(transformed_image)
    display.display()

def main():
    # Define the image sequence and branching logic
    images = {
        1: "images/1.png",
        2: "images/2.png",
        3: "images/3.png",
        4: "images/4.png",
        5: "images/5.png",
        6: "images/6.png",
        7: "images/7.png",
        7.1: "images/7.1.png",
        7.2: "images/7.2.png",
        7.3: "images/7.3.png",
        8: "images/8.png",
        9: "images/9.png",
    }

    current_image = 1  # Start with the first image

    try:
        # Display the initial image
        display_image(images[current_image])

        while True:
            if not up_button.value:  # Up button pressed
                print("Up Button Pushed")
                if current_image == 7:
                    current_image = 8  # Branch 7 -> 8
                elif current_image == 7.1:
                    current_image = 8  # Branch 7.1 -> 8
                elif current_image == 7.2:
                    current_image = 8  # Branch 7.2 -> 8
                elif current_image == 9 or current_image == 7.3:
                    # Reset to the beginning when reaching the end
                    current_image = 1
                elif current_image < 7 or (current_image > 7.3 and current_image < 9):
                    # Move forward normally if not in branching logic
                    current_image += 1

                # Display the new image
                display_image(images[current_image])

            if not down_button.value:  # Down button pressed
                print("Down Button Pushed")
                if current_image == 7:
                    current_image = 7.1  # Branch 7 -> 7.1
                elif current_image == 7.1:
                    current_image = 7.2  # Branch 7.1 -> 7.2
                elif current_image == 7.2:
                    current_image = 7.3  # Branch 7.2 -> 7.3 (end of branch)
                elif current_image > 1 and (current_image <= 7 or current_image > 7.3):
                    # Move backward normally if not in branching logic
                    current_image -= 1

                # Display the new image
                display_image(images[current_image])

    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting cleanly.")

if __name__ == "__main__":
    main()
