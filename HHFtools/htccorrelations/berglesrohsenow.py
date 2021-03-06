# -*- coding: utf-8 -*-
"""
Bergles-Rosenhow equations for ONB and HTC

Created on Tue Feb 16 22:32:29 2016

@author: David
"""

def onb(T_onb,
        water,
        geometry,
        strictness = 'strict'):
    """
    Definition:
        T_onb is the boiling start-up temperature at the wall,
        exceeding the saturation temperature because of an
        overheating of the near-wall saturated water layer.
        It is derived from Bergles-Rohsenow correlation

    Range of Validity:
        0.1 MPa <= P_b <= 13.8 MPa
        
    Formula:
        br = 155500 * (P_b**1.156) * ((1.8*(T_onb-T_sat))**n) - h*(T_onb-T_bulk)
        
    returns:
        br (to be minimised to solve for T_onb)

    """

    from HHFtools.htccorrelations.seidertate import htc as seidertate
    from HHFtools.checks import check_validated

    P_b = water.P

    checks = ('bulk pressure',P_b, 0.1, 13.8)
    check_validated(checks, strictness)

    T_bulk = water.T
    T_sat = water.T_sat
    n = 2.046 / P_b**0.0234
    h = seidertate(water, geometry, T_onb, strictness = 'None')
    br = 155500 * (P_b**1.156) * ((1.8*(T_onb-T_sat))**n) - h*(T_onb-T_bulk)
    return br

def get_T_onb(water,
              geometry):
    """Definition:
        get Temperature at onset of nucleate boiling 
        using berglesrohsenow equation.
    """
    from scipy.optimize import fmin
    
    fn = lambda T: onb(T,water, geometry, strictness='none')

    T_onb = fmin(fn,water.T_sat,disp = 0,ftol = 0.01)[0]
    #print('ping',time.time())
    # print('T_onb = ',T_onb)
    return T_onb


def htc(water,
        geometry,
        T_wall,
        T_onb = 'calculate',
        strictness = 'verbose',
        correlationname = 'Bergles Rohsenow combined'):
    """
    Definition:
        Combined HTC for partial boiling using Seider-Tate and ThomCEA
    """
    from HHFtools.htccorrelations.seidertate import htc as htc_seidertate
    from HHFtools.htccorrelations.thomCEA import htc as htc_thomCEA

    if T_onb == 'calculate':
        T_onb = get_T_onb(water,geometry)
    
    T_bulk  = water.T
    q_singlephase = (T_wall - T_bulk)*(htc_seidertate(water,geometry,T_wall,strictness="None"))
    q_nucleateboiling = (T_wall - T_bulk)*(htc_thomCEA(water,geometry,T_wall))
    q_0 = (T_onb - T_bulk)*(htc_thomCEA(water,geometry, T_onb))
    q_total = ((q_singlephase**2) 
                + (q_nucleateboiling**2)*(1-(q_0/q_nucleateboiling))**2)**0.5
    h = q_total / (T_wall - T_bulk)

    return h

if __name__ == '__main__':
    from HHFtools.classes import test_coolant, test_geometry
    geom = test_geometry()
    water = test_coolant()
    
    for thing in (geom, water):
        print('{:} parameters:'.format(thing.name))
        for attribute in (sorted(thing.__dict__.keys())):
            print('{:25} {:25}'.format(attribute,str(thing.__dict__[attribute])))
        print('*'*45)          
    for Tw in [x for x in range(524,600,10)]:
        print('h({:} K) {:25.2e} W/(m K)'.format(Tw,htc(water, geom,T_wall=Tw)))
    