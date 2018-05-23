# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:41:49 2016

@author: dhancock

many of these can be got from the IAPWS library - but doing this for backup.

"""

from iapws import IAPWS97

def get_reynolds(water,velocity,Dh):
    reynolds = water.rho * velocity * Dh / water.mu
    return reynolds
    
def get_prandlt(water):
    prandlt = water.cp*1000 * water.mu / water.k
    return prandlt
    
def get_boiling_number(heat_flux,mass_flux,latent_heat_of_vaporization):
    boiling_number = heat_flux / (mass_flux*latent_heat_of_vaporization)
    return boiling_number
    
    
if __name__ == '__main__':
    """
    testing
    """    
    
    
    from matplotlib import pyplot as plt
    '''    
    for x in range(1,25):
        water = IAPWS97(T = (273+200), P = x*.1)
        print('{0:2.2} {1:3}'.format(water.P,water.T-273), water.phase)
    for x in range(1,25):
        water = IAPWS97(T = (273+x*10), P = 1.5)
        print('{0:2.4} {1:3}'.format(water.P,water.T-273), water.phase)
    '''
    '''
    fig = plt.figure('test')
    ax = fig.add_subplot(211)
    ax.plot([t+273 for t in range(10,100)],
            [IAPWS97(T = t+273, P =  .4).Pr for t in range(10,100)],
            label = 'Pr for P ='+str(0.4))
    ax.grid('on')
    ax.set_xlabel('T')
    ax.legend()
    ax = fig.add_subplot(212)
    ax.plot([p/10 for p in range(1,10)],
            [IAPWS97(T = 47+273, P =  p/10).Pr for p in range(1,10)],
            label = 'Pr for T = '+str(47+273))
    ax.grid('on')
    ax.legend(loc = 'right')
    ax.annotate('[IAPWS97(T = 320, P = 0.4).Pr = {0:3.2}]'.format(IAPWS97(T = 320, P = 0.4).Pr),xy=(0.15,0.035))
    #fig.show()
    #print(IAPWS97(T = 320, P = 0.4).Pr)
    
    '''
    water=IAPWS97(T = 293, P = .1)
    print('phase:',water.phase)
    print('Pressure = {0}'.format(water.P))
    print('Temperature = {0:3}'.format(water.T))
    print('Pr = {0:3.5}'.format(water.Prandt))

    print('density = {0:1.3e}'.format(water.rho))
    print('mu = {0:2.3e}'.format(water.mu))
    print('Cp = {0:2.3}'.format(water.cp))
    Pr = get_prandlt(water)
    print()
    print('Prandlt = {0:3.5}'.format(Pr))