# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 22:28:03 2016

@author: David
"""

def htc(water,
        geometry,
        T_wall,
        correlationname = 'ITER combined HTC correlation',
        verbose = False):
    """Definition:
        ITER combined HTC correlation
    """

    from HHFtools.htccorrelations.seidertate import htc as htc_seidertate
    from HHFtools.htccorrelations.berglesrohsenow import get_T_onb
    from HHFtools.htccorrelations.berglesrohsenow import htc as htc_berglesrohsenow
    from HHFtools.htccorrelations.tong75 import get_wchf as wchf_tong75



    #print('T_wall = {:}'.format(T_wall))
    T_onb = get_T_onb(water,geometry)

    if T_wall <= T_onb:
        h = htc_seidertate(water,geometry,T_wall,strictness='verbose')
        _fn = 'seidertate only (h={:0.2f})'.format(h)
    else:
        wchf = wchf_tong75(water,geometry)
        if htc_berglesrohsenow(water,geometry,T_wall,T_onb)*(T_wall-water.T) <= wchf:
            h = htc_berglesrohsenow(water,geometry,T_wall, T_onb)
            _fn = 'combined seidertate and ThomCEA '+\
                'using berglesrohsenow (h={:0.2f})'.format(h)
        else:
            h = 0
            print('{:15} = {:15.2f} °C'.format('CHF at T_wall',T_wall-273))
            _fn = 'CHF'

    if verbose is True: print("[T_wall = {}] {}".format(T_wall-273,_fn))
    return h

if __name__ == '__main__':

    from HHFtools.classes import test_geometry, test_coolant
    geom = test_geometry()
    water = test_coolant()
    
    for thing in (geom, water):
        print('{:} parameters:'.format(thing.name))
        for attribute in (sorted(thing.__dict__.keys())):
            print('{:25} {:25}'.format(attribute,str(thing.__dict__[attribute])))
        print('*'*45)          
    for Tw in [x for x in range(300,600,20)]:
        print('h({:} K) {:25.2e} W/(m K)'.format(Tw,htc(water, geom,T_wall=Tw)))