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


def magnitude(ax, ay, az):
    return math.sqrt(ax * ax + ay * ay + az * az) / 9.802


def light_level(a):
    level = 0
    lerp = 0

    if a > 0:
        log2A = math.log(a, 2)
        # Transform from levels -3:4 to 0:10
        level = int((log2A + 3) * 10 / 7)
        lerp = level / 10.0
    return level, lerp


def animate_level(a, maxA):
    if a > 0:
        level, lerp = light_level(a)
        max_level, max_lerp = light_level(maxA)
        for p in range(10):
            if p == max_level:
                cpx.pixels[p] = (int(max_lerp * 255), max(0, int((1.0 - 1.5 * max_lerp) * 255)), 0)
            elif p <= level:
                cpx.pixels[p] = (int(lerp * 255), max(0, int((1.0 - 1.5 * lerp) * 255)), 0)
            else:
                cpx.pixels[p] = (0, 0, 0)


color_index = 0
pixel_number = 0
ax, ay, az = 0, 0, 0
bx, by, bz = 0, 0, 0
dx, dy, dz = 0, 0, 0
max_a = (0, 0)
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

    if not cpx.switch:
        cpx.red_led = not cpx.switch
        log_values(now, ax, ay, az, dx, dy, dz)

    a = magnitude(dx, dy, dz)

    if a > max_a[1]:
        max_a = (now, a)
    elif now - max_a[0] > 2.0:
        max_a = (now, 0)

    animate_level(a, max_a[1])
