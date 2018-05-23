# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:20:23 2017

@author: dhancock
"""

import numpy as np

class PinArray():
    def __init__(self,channelwidth,channelheight,channellength,
                 pin = None, 
                 pinarrangement = None):
        for parm in ("channelwidth","channelheight","channellength"):
            self.__dict__[parm] = locals()[parm]
        self.pin = pin
        self.pin.height = channelheight
        self.pinarrangement = pinarrangement
        if all([x is not None for x in (pin,pinarrangement)]):
            self.get_D_h()
            
    def get_D_h(self):
        """
        ref: 
            Fengming Wang, Jingzhou Zhang, Suofang Wang,
            "Investigation on flow and heat transfer 
            characteristics in rectangular channel 
            with drop-shaped pin fins",
            Propulsion and Power Research 2012;1(1):64–70
        """
        B = self.channelwidth
        H = self.channelheight
        L = self.channellength
        N = self.pinarrangement.number
        A_p = self.pin.area
        L_p = self.pin.circumference
        
        V_f = B * H * L - N * A_p * H
        A_f = 2 * (B + H) * L + N * (L_p * H - 2 * A_p)
        
        self.D_h = 4 * V_f / A_f

class Pin():
    def __init__(self,shape,**kwargs):
        for arg in kwargs.keys():
            self.__dict__[arg] = kwargs[arg]

        assert shape in ("circular",), "unsupported pin shape"
        if shape=="circular":
            self.area = np.pi*(self.diameter/2)**2
            self.circumference = np.pi*self.diameter

    
class PinArrangement():
    def __init__(self,**kwargs):
        for arg in kwargs.keys():
            self.__dict__[arg] = kwargs[arg]

"""
if __name__ is "__main__":
    
    import HHFtools
    
    channel = HHFtools.Geometry(shape="rectangular channel",
                                channelwidth = 20e-3,
                                channelheight = 5e-3,
                                length = 1)
    water = HHFtools.Coolant(T=273+100, P=1, velocity=10)
    pin = Pin("circular",diameter = 1e-3)
    arrangement = PinArrangement(dx = 2e-3,
                              dy = 2e-3,
                              nx = 2,
                              ny = 4)
    pinarray = PinArray(20e-3,5e-3,50e-3,pin,arrangement)
""" 
    