import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

import sys
import numpy as np

class PixelStrip:


    def on_close(self, event):
        print("Figure closed. Terminating program...")
        self.closed = True  # don't call sys.exit() here


    def __init__(self, led_count: int):

        self.closed = False
        self.led_count = led_count

        self.led_states=[(0,0,0)]*led_count
        
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        plt.ion()


        # x positions never change, so set them up once
        x = np.arange(self.led_count)
        y = np.zeros(self.led_count)

        # single scatter artist for all LEDs, colors updated per-frame
        self.scatter = self.ax.scatter(
            x, y,
            s=25,               # roughly equivalent to markersize=5
            facecolor='none',
            edgecolor='white',
            linewidth=0.1,
            animated=True,      # tell mpl not to include it in normal draws
        )


        self.ax.set_facecolor('black')
        self.ax.set_title('LED Simulator')

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-1, self.led_count)
        self.ax.set_ylim(-1, 1)

        # draw everything once, then cache the static background
        plt.show(block=False)
        self.fig.canvas.draw()
        plt.pause(0.01)  # let the window actually render/map
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)        


    @staticmethod
    def get_plt_color_code(color_code):
        return color_code / 255


    def set_pixel_color(self, led_index, led_rgb):

        #  end program on figure exit
        if self.closed:
            return  # bail out early instead of touching a dead canvas


        #  scale RGB code to matplotlib syntax requirements
        led_color = (
            self.get_plt_color_code(led_rgb[0]),
            self.get_plt_color_code(led_rgb[1]),
            self.get_plt_color_code(led_rgb[2]),
        )


        #  define color at led position
        self.led_states[led_index]=led_color


    def show_led_strip(self):

        #  end program if plot exit
        if self.closed:
            return  # bail out early instead of touching a dead canvas


        # update the existing artist instead of creating new ones
        self.scatter.set_facecolor(self.led_states)
        self.scatter.set_edgecolor((1, 1, 1))


        # blit: restore static background, draw only the scatter, push to screen
        self.fig.canvas.restore_region(self.background)
        self.ax.draw_artist(self.scatter)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()