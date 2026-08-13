from operator import itemgetter

from matplotlib import pyplot as plt
import numpy as np
import math

class ColorPicker:


    def __init__(self):
        pass


    def get_rgb(self, theta):

        #  theta (degrees) is the angle on a color wheel - assume angles as defined on a unit circle


        #  calculate RGB values based on the theta input
        def get_blue(theta):
            return 382.5*np.sin(((math.pi/180)*theta)-(2*math.pi/3))+127.5

        def get_red(theta):
            return 382.5*np.sin(((math.pi/180)*theta)-(2*math.pi/3)+((math.pi/180)*120))+127.5
        
        def get_green(theta):
            return 382.5*np.sin(((math.pi/180)*theta)-(2*math.pi/3)-((math.pi/180)*120))+127.5
        

        #  store calculated RGB values in a tuple
        rgb_calc = (get_red(theta), get_green(theta), get_blue(theta))


        #  cap each calculated RGB value at 255, which is the maximum RGB value
        #  store RGB in a class variable
        self.rgb = ()
        for color in rgb_calc:

            if color>255:
                color = 255
            elif color<0:
                color = 0

            color = float(color)
            self.rgb = self.rgb+(color,)
