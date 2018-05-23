# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 16:39:31 2016

@author: dhancock
"""

def flashing_fraction(water,vesselpressure,verbose = False):
    """
    Function:
        provides a flashing fraction value
    Note:
        
        only valid for water!
        (uses IAPWS97 values internally)
    """
    from HHFtools import Coolant
    Tu = water.T
    C_p = water.cp*1000
    Td = Tsat = Coolant(P = vesselpressure, x = 1).T
    steam = Coolant(T = Tsat, P = vesselpressure)
    Hv = steam.ifg
    X = C_p*(Tu-Td) / Hv
    
    if verbose is True:
        print('-'*40)
        print('Water: {:10.1f} °C, {:10.2f} Bar'.format(water.T-273, water.P*10))
        print('Steam: {:10.1f} °C, {:10.2f} Bar'.format(steam.T-273, steam.P*10))
        print('-'*40)
        print('C_p = {:12.2f} J/(kg °C)'.format(C_p))
        print('Hv  = {:12.2e} J/kg'.format(Hv))
        print('X   = {:12.2f} %'.format(X*100))
        
    return X

def plot_flashing_fraction(tmin,tmax,vesselpressure,step=1):
    """
    Note:
        uses a 15°C overhead pressure on the coolant, as per the ICS unit.
    """
    from HHFtools import Coolant
    from matplotlib import pyplot as plt
    from numpy import arange

    t = arange(tmin,tmax,step)
    temp_overhead = 15
    x = [flashing_fraction(Coolant(T=temp+273,
                                   P=Coolant(T=temp+273+temp_overhead,x=0).P),
                                   vesselpressure,False)*100 \
                                        for temp in t]
    fig = plt.figure('flashing fraction')
    ax = fig.add_subplot(111)
    ax.plot(t,x)
    ax.plot(t,[8.6]*len(t))
    ax.grid('on')
    ax.set_xlabel('Coolant temperature [°C]')
    ax.set_ylabel('Flashing Fraction [%]')
    ax.set_title('Flashing fraction with temperature'+\
                '\n(vessel pressure = {:0.1f} Bar)'.format(vesselpressure*10))
    fig.show()


if __name__ == '__main__':
    vesselpressure =.15
    plot_flashing_fraction(100,200,vesselpressure)