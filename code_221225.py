import time
import terminalio
import board
import neopixel
import touchio
import displayio
import adafruit_ssd1680
from adafruit_display_text import  label
from adafruit_bitmap_font import  bitmap_font
from rainbowio import colorwheel


# Function for append text to the display data
def _addText(text, scale, color, x_cord, y_cord):
    group = displayio.Group(scale=scale, x=x_cord, y=y_cord)
    #text_label = label.Label(terminalio.FONT, text=text, color=color)
    text_label = label.Label(font, text=text, color=color)
    group.append(text_label)
    display_data.append(group)


# Define board pinout
board_spi = board.SPI()  # Uses SCK and MOSI
board_epd_cs = board.D41
board_epd_dc = board.D40
board_epd_reset = board.D39
board_epd_busy = board.D42

# Define touch buttons
touch_threshold = 20000
touch_1 = touchio.TouchIn(board.D5)
touch_1.threshold = touch_threshold
touch_2 = touchio.TouchIn(board.D4)
touch_2.threshold = touch_threshold
touch_3 = touchio.TouchIn(board.D3)
touch_3.threshold = touch_threshold
touch_4 = touchio.TouchIn(board.D2)
touch_4.threshold = touch_threshold
touch_5 = touchio.TouchIn(board.D1)
touch_5.threshold = touch_threshold


# Define LED colors value
led_off = (0, 0, 0)
led_red = (255, 0, 0)
led_green = (0, 255, 0)
led_blue = (0, 0, 255)
led_yellow = (255, 255, 0)
led_white = (255, 255, 255)

# Define LED
led_pin = board.D18
led_matrix = neopixel.NeoPixel(led_pin, 4, brightness=0.1, auto_write=False)


# Define ePaper display colors value
display_black = 0x000000
display_white = 0xFFFFFF

# Define ePaper display resolution
display_width = 250
display_height = 122

# Prepare ePaper display
displayio.release_displays()
display_bus = displayio.FourWire(
    board_spi,
    command=board_epd_dc,
    chip_select=board_epd_cs,
    reset=board_epd_reset,
    baudrate=1000000,
)
time.sleep(1)
display = adafruit_ssd1680.SSD1680(
    display_bus,
    width=display_width,
    height=display_height,
    rotation=270,
    busy_pin=board_epd_busy,
)
display_data = displayio.Group()
display_background = displayio.Bitmap(display_width, display_height, 1)
display_color_palette = displayio.Palette(1)
display_color_palette[0] = display_white

font_file = "fonts/VWBrochure-21.bdf"

bmp_file = displayio.OnDiskBitmap("qr_test.bmp")

font = bitmap_font.load_font(font_file)

# Append tilegrid with the background to the display data
display_data.append(
    displayio.TileGrid(display_background, pixel_shader=display_color_palette)
)

#
# Create a TileGrid to hold the bitmap
tile_grid_bmp = displayio.TileGrid(bmp_file, pixel_shader=bmp_file.pixel_shader)

# Create a Group to hold the TileGrid
#group = displayio.Group()

# Add the TileGrid to the Group
display_data.append(tile_grid_bmp)

# Add the Group to the Display
#display.show(group)
#

# Render namecard to display
_addText("Honza", 1, display_black, 130, 20)
_addText("Marek", 1, display_black, 130, 50)
#_addText("+420 604 487 147", 1, display_black, 1, 70)
# _addText("Time Is:{}".format(time.monotonic()), 2, display_black, 10, 60)
#_addText("@tarmara1981", 1, display_black, 120, 90)
#_addText("tarmara@seznam.cz", 1, display_black, 5, 110)
#_addText("Lysa nad Labem", 1, display_black, 30, 110)

display.show(display_data)
display.refresh()

# MAIN LOOP
while True:
    if touch_1.value:
        # Turn off the LED
        led_matrix.fill(led_off)
        led_matrix.show()
    if touch_2.value:
        # Set LED to red
        led_matrix[0] = led_yellow  # right up
        led_matrix[1] = led_red  # left up
        led_matrix[2] = led_green  # left down
        # led_matrix[3].brightness = 0.1 - nefunguje
        led_matrix[3] = led_blue  # right down
        led_matrix.show()
    if touch_3.value:
        # Set LED to green
        """
        led_matrix.fill(led_green)
        led_matrix.show()
        """
        i = 0
        pal = 255
        loop = 5
        led_matrix.deinit()  # pokud chci prenastavit jas, tak musim odinicializovat diody a inicializovat je znovu
        led_matrix = neopixel.NeoPixel(led_pin, 4, brightness=0.2, auto_write=False)
        """
        while i <= n:
            led_matrix.fill(colorwheel((time.monotonic() * 50) % 255))
            led_matrix.show()
            time.sleep(0.1)
            i = i + 1
        """
        while i <= pal * loop:
            led_matrix.fill(colorwheel(i))
            led_matrix.show()
            time.sleep(0.01)
            i = i + 1

    if touch_4.value:
        # Set LED to blue
        led_matrix.deinit()  # pokud chci prenastavit jas, tak musim odinicializovat diody a inicializovat je znovu
        num_leds = 4
        led_matrix = neopixel.NeoPixel(
            led_pin, num_leds, brightness=0.2, auto_write=False
        )
        delta_hue = 256 // num_leds
        speed = 10  # higher numbers = faster rainbow spinning
        r = 0
        i = 1
        n = 100
        while i <= n:
            for l in range(len(led_matrix)):
                led_matrix[l] = colorwheel(int(r * speed + l * delta_hue) % 255)
            led_matrix.show()  # only write to LEDs after updating them all
            r = (r + 1) % 255
            time.sleep(0.05)
            i = i + 1

    if touch_5.value:
        # Set LED to white
        led_matrix.deinit()
        led_matrix = neopixel.NeoPixel(led_pin, 4, brightness=0.2, auto_write=False)
        led_matrix.fill(led_white)
        led_matrix.show()
