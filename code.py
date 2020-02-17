"""For a detailed guide on all the features of the Circuit Playground Express (cpx) library:
https://adafru.it/cp-made-easy-on-cpx"""
import math
import time
import microcontroller
from adafruit_circuitplayground.express import cpx

# Set TONE_PIANO to True to enable a tone piano on the touch pads!
TONE_PIANO = True

# Set this as a float from 0 to 1 to change the brightness.
# The decimal represents a percentage.
# So, 0.3 means 30% brightness!
cpx.pixels.brightness = 1.0

# Changes to NeoPixel state will not happen without explicitly calling show()
cpx.pixels.auto_write = True


def log_values(now, ax, ay, az, dx, dy, dz):
    try:
        with open("/data.csv", "a") as fp:
            # do the C-to-F conversion here if you would like
            fp.write("%f,%f,%f,%f,%f,%f,%f\n" % (now, ax, ay, az, dx, dy, dz))
            fp.flush()
            cpx.red_led = not cpx.red_led
    except OSError as e:
        delay = 1
        if e.args[0] == 28:
            delay = 2
        while True:
            cpx.red_led = not cpx.red_led
            print(e)
            time.sleep(delay)


def animation(now, start, ax, ay, az):
    a = math.sqrt(ax * ax + ay * ay + az * az)
    a = a / 9.802

    if a > 0:
        log2A = math.log(a, 2)
        # Transform from levels -3:4 to 0:10
        level = int((log2A + 3) * 10 / 7)
        lerp = level / 10.0
        #  print(level, lerp, a)
        for p in range(10):
            if p <= level:
                cpx.pixels[p] = (int(lerp * 255), int((1.0 - lerp) * 255), 0)
            else:
                cpx.pixels[p] = (0, 0, 0)


color_index = 0
pixel_number = 0
ax, ay, az = 0, 0, 0
bx, by, bz = 0, 0, 0
dx, dy, dz = 0, 0, 0
# time.monotonic() allows for non-blocking LED animations!
start = time.monotonic()
while True:
    now = time.monotonic()
    # If the switch is to the left, it returns True!
    cpx.red_led = cpx.switch

    bx, by, bz = ax, ay, az
    ax, ay, az = cpx.acceleration
    dx, dy, dz = (ax - bx), (ay - by), (az - bz)
    print(now, ax, ay, az, dx, dy, dz)
    log_values(now, ax, ay, az, dx, dy, dz)
    animation(now, start, dx, dy, dz)

    # Press the buttons to play sounds!
    if cpx.button_a:
        cpx.play_file("drama.wav")
    elif cpx.button_b:
        cpx.play_file("low_fade.wav")
