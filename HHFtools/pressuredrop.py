# -*- coding: utf-8 -*-
"""
pressure drop calculations
Created on Mon Feb 29 10:03:12 2016

@author: dhancock

"""
## list of all 'useful' functions to ease importing

__all__ = ['friction_factor',
           'loss_coefficient',
           'pressure_loss',
           'dynamic_pressure']

#%% MAIN FUNCTIONS

def friction_factor(coolant,geometry):
    """
    Description:
        Function Written to find the friction factor
        given as D.10 & D.11 in ECP book, (Colebrook White)
        [Taken from R Bamber 23 Avril 2014]
    Inputs:
        coolant,
        geometry
    """
    import math
    Re = coolant.Reynolds(geometry.D_h)
    relative_roughness = geometry.relative_roughness

    laminar = 64 /Re

    A = (2.457 * math.log(1 / ((7 / Re)**0.9 + 0.27 * relative_roughness)))**16
    B = (37530 / Re)**16
    turbulent = 8 * ((8 / Re)**12 + (A + B)**(-1.5))**(1 / 12)

    if Re < 2000:
        ffactor = laminar
    if Re > 4000:
        ffactor = turbulent
    else:
        ffactor = laminar + (Re - 2000) / 2000 * (turbulent - laminar)

    return ffactor

def loss_coefficient(coolant, geometry):
    """Loss coefficient calculator:

    Source:
        Taken from Rob's spreadsheet!

    Description:
        if the provided geometry has a loss_coefficient already defined,
        it just returns this value.

        For straight sections, loss coefficient = friction factor * l/D

        For bends, a "bend contribution" is added = bend_radius/pipediameter * angle/90

        The function BOTH returns the loss coefficient and assigns it to the geometry.
    """
    if geometry.shape == 'instrument' and 'loss_coefficient' in geometry.__dir__():
        loss_coefficient = geometry.loss_coefficient
        return loss_coefficient

    ffactor = friction_factor(coolant,geometry)

    length = geometry.length
    D_h = geometry.D_h

    loss_coefficient = geometry.loss_coefficient = ffactor * length / D_h

    ## this is a very rough estimate!
    if 'bendsangle' not in geometry.__dir__():
        geometry.bendsangle = 0
    if geometry.bendsangle !=0:
        if 'bend_contribution' not in geometry.__dir__():
            geometry.bend_contribution = ffactor\
                *geometry.bend_radius/geometry.pipediameter\
                *geometry.bendsangle/90
        geometry.loss_coefficient += geometry.bend_contribution
        loss_coefficient = geometry.loss_coefficient
    return loss_coefficient

def pressure_loss(coolant,geometry):
    """
    Calculation:
        pressure loss = density * loss_coefficient * V^2 / 2
    Returns:
        pressure loss in MPa
    """
    p_loss = coolant.rho*loss_coefficient(coolant,geometry)\
                                                *0.5*coolant.velocity**2 / 1e6
    return p_loss

def dynamic_pressure(coolant,geometry):
    coolant.get_velocity(geometry)
    coolant.p_dynamic = p_dynamic = 0.5 * coolant.rho * coolant.velocity**2
    coolant.geometryname = geometry.name

    return p_dynamic

#%% TESTS

def simple_test(temperature = 100,
                pressure = 5,
                diameter = 10e-3,
                length = .3,
                flow = 50, # l / min
                roughness = 5e-6,
                angle = 180,
                loverd = 12):

    from HHFtools import Coolant, Geometry

    # define core values
    coolant = Coolant(P = pressure,
                      T = temperature+273,
                      flow_lpm = flow)

    geometry = Geometry(shape = 'smooth tube',
                        pipediameter = diameter,
                        length = length)

    velocity = coolant.get_velocity(geometry=geometry)

    ## add pressure specific values
    geometry.set_roughness(roughness)
    geometry.bendsangle = angle
    geometry.bend_loverd = loverd

    ## print some coolant parameters
    for item in ['T', 'P', 'velocity']:
        print('{:20} ={:>31.2f}'\
            .format(item,coolant.__dict__[item]))
    for item in ['rho','mu']:
        print('{:20} ={:>31.3e}'\
            .format(item,coolant.__dict__[item]))
    print('*'*60)

    ## print some geometry parameters
    for item in ['D_h', 'length', 'area','relative_roughness']:
        print('{:20} ={:>31.5f}'\
            .format(item,geometry.__dict__[item]))
    print('*'*60)

    ## print Re
    print('{:}(D_h={:})\t     ={:>31.2f}'\
        .format('Re',geometry.D_h,coolant.Reynolds(geometry.D_h)))
    print('*'*60)

    ## print the outputs from this module
    for fn in [friction_factor,loss_coefficient,pressure_loss]:
        print('{:20} ={:>31.4f}'.format(fn.__name__,fn(coolant,geometry)))

    return locals()

def rob_compare(generalisations = False):
    """
    checks against rob's pressure drop sheet for the rig

    """
    from HHFtools import Coolant, Geometry

    t = 200+273
    p = 20
    flow = 100
    names = ['main line','flexibles','sample','f\'through']
    diameters = [i*1e-3 for i in (40,25,10,21)]
    lengths = [5,2,.3,1.5]
    bends = [i*90 for i in (8,2,4,4)]
    roughness = 5e-6

    coolant = Coolant(T=t,P=p,flow_lpm=flow)
    pd = []
    velocities = []

    for i,d in enumerate(diameters):
        l = lengths[i]
        b = bends[i]
        geometry = Geometry(shape = 'smooth tube',
                        pipediameter = d,
                        length = l,
                        bendsangle = b)
        geometry.set_roughness(roughness)

        ## corrections to match Rob's generalisations
        if generalisations is True:
            geometry.relative_roughness = 0.00225
            coolant.rho = 1000
            coolant.mu = 5e-4

        coolant.get_velocity(geometry=geometry)
        velocities.append(coolant.velocity)
        p = pressure_loss(coolant,geometry)
        pd.append(p)

    extras = 1.5/10
    pd_total = sum(pd)+extras

    print('{:10}{:>15}{:>15}{:>15}{:>15}{:>15}{:>10}'.format('Linesection',
                                                        'dP [bar]',
                                                        'ID [mm]',
                                                        'Bends [x90°]',
                                                        'Length [m]',
                                                        'velocity [m/s]',
                                                        '%dP'))
    print('_'*95)
    for i,d in enumerate(diameters):
        n = names[i]
        p = pd[i]
        ## d already set
        b = bends[i]
        l = lengths[i]
        v = velocities[i]
        pc = pd[i]/pd_total *100

        print('{:10}:{:15.3f}{:15}{:15}{:15}{:15.2f}{:10.1f}'\
                    .format(n,p*10,d*1000,b/90,l,v,pc))
    print('{:20} {:5.3f}{:70.1f}'\
                    .format('Extras  :',extras*10,extras/pd_total*100))
    print('_'*95)
    print('{:20}{:5.2f}'.format('Total  :',pd_total*10))


#%%  STANDALONE

if __name__ == '__main__':
    from HHFtools import Coolant, Geometry
    #print('\n')
    #print('SIMPLE_TEST()')
    #simple_test()
    #print('\n')
    #print('Comparison with Rob\'s spreadsheet:'.upper())

    rob_compare(generalisations=True)
    coolant = Coolant(T=293,P=0.1, velocity = 10)
    geometry = Geometry(shape = 'smooth tube', pipediameter = 10e-3)
    p_dynamic = dynamic_pressure(coolant,geometry)
    print('Dynamic pressure = {:0.4} MPa'.format(p_dynamic/1000))

