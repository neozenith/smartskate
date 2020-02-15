import storage
from adafruit_circuitplayground.express import cpx

cpx.red_led = cpx.switch
storage.remount("/", cpx.switch)
