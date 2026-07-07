"""
Basic WS2812B (NeoPixel) driver test for Raspberry Pi Pico + MicroPython.

Wiring:
  Pico GPIO0 -> ~330 ohm resistor -> level shifter data in
  Level shifter data out          -> strip DIN
  5V power supply +               -> strip 5V (through ~1000uF cap)
  5V power supply -, Pico GND,
    level shifter GND, strip GND  -> all tied together (common ground)

Install: this uses the built-in 'neopixel' module, included with
standard MicroPython builds for the Pico. No extra install needed.
"""

from machine import Pin
import neopixel
import time

NUM_LEDS = 30      # change to match your strip length
DATA_PIN = 0        # GPIO0

np = neopixel.NeoPixel(Pin(DATA_PIN), NUM_LEDS)


def clear():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()


def solid_color(r, g, b):
    for i in range(NUM_LEDS):
        np[i] = (r, g, b)
    np.write()


def rainbow_cycle(wait=0.02, cycles=3):
    for j in range(256 * cycles):
        for i in range(NUM_LEDS):
            pixel_index = (i * 256 // NUM_LEDS) + j
            np[i] = wheel(pixel_index & 255)
        np.write()
        time.sleep(wait)


def wheel(pos):
    # Generates rainbow colors across 0-255 positions.
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)


def chase(color, wait=0.05):
    clear()
    for i in range(NUM_LEDS):
        np[i] = color
        np.write()
        time.sleep(wait)
        np[i] = (0, 0, 0)


if __name__ == "__main__":
    print("Starting WS2812B test...")

    print("Solid red")
    solid_color(255, 0, 0)
    time.sleep(1)

    print("Solid green")
    solid_color(0, 255, 0)
    time.sleep(1)

    print("Solid blue")
    solid_color(0, 0, 255)
    time.sleep(1)

    print("Chase")
    chase((255, 255, 255), wait=0.03)

    print("Rainbow cycle")
    rainbow_cycle(wait=0.005, cycles=1)

    clear()
    print("Done.")
