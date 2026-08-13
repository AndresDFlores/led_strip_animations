import time
import math

from pixel_strip import *
from color_wheel import *


#  global variables
led_count=75
strip = PixelStrip(led_count)
color_wheel = ColorPicker()


def crawl(led_color:tuple=(255, 255, 255), trigger_duration=5):

    #  how long to wait between each LED definition iteration
    iter_delay = trigger_duration / led_count

    for current_led_idx in range(led_count):

        #  end program on figure exit
        if strip.closed:
            break

        #  write LED state to memory, define on color
        strip.set_pixel_color(
            led_index=current_led_idx, 
            led_rgb=led_color)  # _set_pixel(i, r, g, b)

        #  write LED states to strip
        strip.show_led_strip()  # strip.show()

        #  hold for next loop to start
        time.sleep(iter_delay)

        #  write LED state, define off
        strip.set_pixel_color(
            led_index=current_led_idx, 
            led_rgb=(0,0,0))  # _set_pixel(i, r, g, b)


def crawl_loop(led_color:tuple=(255,255,255), iter_delay=0):

    loop_idx=0
    while True:

        #  end program on figure exit
        if strip.closed:
            break

        #  LED index in focus
        current_led_idx = loop_idx%led_count

        #  write LED state to memory, define on color
        strip.set_pixel_color(
            led_index=current_led_idx, 
            led_rgb=led_color)  # _set_pixel(i, r, g, b)

        #  strip.show()
        strip.show_led_strip()

        #  hold for next loop to start
        time.sleep(iter_delay)

        #  index next LED on iteration
        loop_idx+=1

        #  write LED state, define off    
        strip.set_pixel_color(
            led_index=current_led_idx, 
            led_rgb=(0,0,0))  # _set_pixel(i, r, g, b)


def comet_loop(led_color:tuple=(255,255,255), iter_delay=0):

    #  define tail LED scaling
    comet_tail_length = 20  #  how many LEDs will make up the comet tail
    comet_tail_scaler_array = [1/(idx+1) for idx in range(comet_tail_length)]  # list comprehension

    loop_idx=0
    while True:

        #  end program on figure exit
        if strip.closed:
            break

        #  LED index in focus
        current_led_idx = loop_idx%led_count

        #  write LED state to memory, define on color
        strip.set_pixel_color(
            led_index=current_led_idx, 
            led_rgb=led_color)  # _set_pixel(i, r, g, b)

        #  define comet tail colors
        for comet_tail_led_trailing_idx in range(comet_tail_length):

            tail_idx = current_led_idx-comet_tail_led_trailing_idx
            if tail_idx>=0:
                scaler = comet_tail_scaler_array[comet_tail_led_trailing_idx]
                scaled_color = (led_color[0]*scaler, led_color[1]*scaler, led_color[2]*scaler)

                #  write LED state to memory, define on color
                strip.set_pixel_color(
                    led_index=tail_idx, 
                    led_rgb=scaled_color)  # _set_pixel(i, r, g, b)


        #  turn off LED after comet tail has passed
        led_off_idx = (tail_idx-1)%led_count


        #  write LED state, define off
        strip.set_pixel_color(
            led_index=led_off_idx, 
            led_rgb=(0,0,0))  # _set_pixel(i, r, g, b)

        #  strip.show()
        strip.show_led_strip()

        #  hold for next loop to start
        time.sleep(iter_delay)

        #  index next LED on iteration
        loop_idx+=1


def crawl_rainbow(step:int=1, iter_delay=0):

    loop_idx=0
    while True:

        #  end program on figure exit
        if strip.closed:
            break

        #  overlay LED strip on color wheel to assign color to each pixel
        for current_led_idx in range(led_count):

            #  evenly distribute LEDs along the color wheel + color wheel rotation increment
            pixel_idx = (current_led_idx * 256 // led_count) + loop_idx

            #  define pixel color
            color_wheel.get_rgb(pixel_idx%256)
            r, g, b = color_wheel.rgb

            #  write LED state to memory, define on color
            strip.set_pixel_color(
                led_index=current_led_idx, 
                led_rgb=(r,g,b))  # _set_pixel(i, r, g, b)

        #  strip.show()
        strip.show_led_strip()

        #  hold for next loop to start
        time.sleep(iter_delay)

        #  shift all LEDs 1 color increment (gives the flow effect)
        #  step indicates magnitude of shift along color wheel, which influences flow rate
        loop_idx = (loop_idx - step) % 256


try:    
    # crawl()
    # crawl_loop(iter_delay=.02)
    # comet_loop(led_color=(255, 0, 255), iter_delay=.02)
    crawl_rainbow(step=10, iter_delay=0.02)

        
except KeyboardInterrupt:
    plt.ioff()
    plt.show()


plt.show()
