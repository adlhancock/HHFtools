# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 22:27:06 2016

@author: David
"""


def htc_plot(htccorrelation,
                       water,
                       geometry,
                       temprange = (25+273,300+273),
                       stepsize = 5):

    from numpy import arange
    from matplotlib import pyplot as plt
    from berglesrohsenow import get_T_onb

    walltemperatures = arange(min(temprange),max(temprange),stepsize)
    hs = [htccorrelation(water,geometry,T_w) for T_w in walltemperatures]

    fig = plt.figure(htccorrelation.__module__)
    ax = fig.add_subplot(111)
    graphtitle = ('{0}'.format(htccorrelation.__module__))
    ax.set_title(graphtitle)
    ax.set_xlabel('T_w [°C]')
    ax.set_ylabel('h [W.m^2.K^-1]')

    plotlabel =  'P={:}MPa\nT={:}°C\nV={:}m/s\ngeom={}\nD_h={:2.2}m'\
                                                        .format(water.P,
                                                                water.T-273,
                                                                water.velocity,
                                                                geometry.shape,
                                                                geometry.D_h)
    htcline = ax.plot([x-273 for x in walltemperatures],hs,
            label = plotlabel)

    T_sat_C = water.T_sat-273
    T_onb_C = get_T_onb(water,geometry)-273
    ax.plot([T_sat_C]*2,[hs[0],max(hs)],
                        '--r',
                        label = 'T_sat ({:0.2f})'.format(T_sat_C))
    ax.plot([T_onb_C]*2,[hs[0],max(hs)],
                        '--g',
                        label = 'T_onb ({:0.2f})'.format(T_onb_C))

    # ax.set_ylim([hs[0]*0.75,max(hs)*1.25])
    ax.set_ylim([0,3e5])
    ax.grid('on')
    ax.legend(loc = 2)
    fig.show()
    return fig

def print_quantities(water,geometry):

    from berglesrohsenow import get_T_onb
    from tong75 import get_wchf as tong75

    print('*'*45)
    #print('{:15} = {:>15}'.format('Geometry shape',geometry.shape))
    for attribute in geometry.__dict__:
        print('{:15} = {:>15}'.format(attribute,
                                      str(geometry.__dict__[attribute])))
    print('*'*45)
    print('{:15} = {:>15.2f} °C'.format('T_sat',water.T_sat-273))
    print('{:15} = {:>15f}'.format('water.mu',water.mu))
    print('{:15} = {:>15f}'.format('water.cp',water.cp))
    print('{:15} = {:>15f}'.format('water.k',water.k))
    print('{:15} = {:>15f}'.format('water.rho',water.rho))
    print('{:15} = {:>15.2f}'.format('water.ifg',water.ifg))
    print()
    print('{:15} = {:>15.2f} °C'.format('T_onb',
                                        get_T_onb(water,geometry)-273))
    print()
    print('{:15} = {:>15f}'.format('water.Reynolds',
                                    water.Reynolds(geometry = geometry)))
    print('{:15} = {:>15f}'.format('water.Prandt',water.Prandt))
    print('{:15} = {:>15.2f} W m^-2 K^-1'.format('WCHF',
                                                 tong75(water,geometry)))
    print('*'*45)

if __name__ == '__main__':

    import HHFtools
    import time

    from HHFtools.classes import Geometry, Coolant, test_coolant, test_geometry
    from ITER import htc as ITER_combined
    from seidertate import htc as seidertate
    #from thomCEA import htc as thomCEA

    tic = time.time()

    coolants = []
    coolants.append(test_coolant())    
    #coolants.append(Coolant(T = 373, P = 4, V = 10))

    geometries = []
    geometries.append(test_geometry())
    #geometries.append(Geometry(shape = 'twisted tape',twistratio = 2,pipediameter = 10e-3,tapethickness = .8e-3))
    #geometries.append(Geometry(shape = 'smooth tube', pipediameter = 8e-3))
    dT = 10

    for water in coolants:        
        for geometry in geometries:
            plotcombined = htc_plot(ITER_combined,water,geometry,temprange = [x+273 for x in (25,320)],stepsize = dT)
            #plotstonly = htc_plot(seidertate,water,geometry,temprange = [x+273 for x in (25,240)],stepsize = dT)
            print_quantities(water,geometry)
        print()
    
    print('{:15}={:>10.4} seconds'.format('Calc time',time.time()-tic))
    del tic


