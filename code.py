"""For a detailed guide on all the features of the Circuit Playground Express (cpx) library:
https://adafru.it/cp-made-easy-on-cpx"""
import time
import microcontroller
from adafruit_circuitplayground.express import cpx

# Set TONE_PIANO to True to enable a tone piano on the touch pads!
TONE_PIANO = True

# Set this as a float from 0 to 1 to change the brightness.
# The decimal represents a percentage.
# So, 0.3 means 30% brightness!
cpx.pixels.brightness = 0.4

# Changes to NeoPixel state will not happen without explicitly calling show()
cpx.pixels.auto_write = True


def animation(now, start):

    # Red-comet rainbow swirl!
    for p in range(10):
        cpx.pixels[p] = (0, 0, 0)
        cpx.pixels[p] = (int(now) % 255, p * 25, 255 - 25 * p)


color_index = 0
pixel_number = 0
ax, ay, az = 0, 0, 0
bx, by, bz = 0, 0, 0
dx, dy, dz = 0, 0, 0
# time.monotonic() allows for non-blocking LED animations!
start = time.monotonic()
while True:
    now = time.monotonic()
    print(int(now) % 255)
    animation(now, start)
    # If the switch is to the left, it returns True!
    cpx.red_led = cpx.switch

    bx, by, bz = ax, ay, az
    ax, ay, az = cpx.acceleration
    dx, dy, dz = (ax - bx), (ay - by), (az - bz)
    print(now, ax, ay, az, dx, dy, dz)

    # Press the buttons to play sounds!
    if cpx.button_a:
        cpx.play_file("drama.wav")
    elif cpx.button_b:
        cpx.play_file("low_fade.wav")
