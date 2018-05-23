# -*- coding: utf-8 -*-
"""
IRtools:
========

Created on Fri Apr 22 14:55:12 2016
@author: David
"""


def e_planck(T,ll):
    e = 2.718281828459045
    c = 299792458
    h = 6.62607004e-34
    k = 1.38064852e-23

    E = 2*h*c**2 / ll**5 * 1/(e**(h*c/(ll*k*T))-1)

    return E


def e_planck_plot(T,normalised=False):
    from numpy import arange
    from matplotlib import pyplot as plt

    number_points = 100
    llmin, llmax = .1, 10
    ll_values = [ll*1e-6 for ll in arange(llmin,
                                        llmax,
                                        (llmax-llmin)/(number_points))]
    e_values = [e_planck(T,ll) for ll in ll_values]
    e_normalised = [e/max(e_values) for e in e_values]

    if normalised is True:
        e_values = e_normalised
    e_max = max(e_values)
    ll_max = ll_values[e_values.index(e_max)]

    plt.plot(ll_values,e_values,label='{:0.0f} K'.format(T))
    plt.plot(ll_max,e_max,'x')
    plt.annotate('({0:0.2e} um, {1:0.2e})'.format(ll_max/1e-6,e_max),xy = (ll_max,e_max))
    plt.legend()
    plt.grid('on')

    return ll_max, e_max

def transmission_plot(material):
    pass


if __name__ == '__main__':
    from matplotlib.pyplot import clf
    clf()
    for T in [200,500,800,1000]:
        #T = 273+800
        ll = 6.0e-6
        E = e_planck(T,ll)
        #print('E(T = {:},ll = {:}) = {:0.3e}'.format(T,ll,E))
        ll_max, e_max = e_planck_plot(T)
        #print('{:} C:\t{:0.2f} um \t {:0.2e}'.format(T,ll_max/1e-6,e_max))
