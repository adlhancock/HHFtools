# -*- coding: utf-8 -*-
"""
HHFtools:
=========
    A set of tools for handling HHF structures
    includes a number of heat transfer correlations and pressure drop calculations

.. py:module:: HHFtools

.. moduleauthor:: adlhancock
"""
__all__ = ['Coolant',
           'Geometry',
           'Pin', 'PinArrangement', 'PinArray'
           'htccorrelations',
           'pressuredrop',
           'IRtools',
           'nondimensionalnumbers',
           'flashing_fraction',
           'checks']

from HHFtools.classes import Coolant, Geometry, Pin, PinArrangement, PinArray
from HHFtools.htccorrelations import htc_ITER
from HHFtools.htccorrelations import htc_seidertate
from HHFtools.htccorrelations.display import print_quantities, htc_plot
from HHFtools.htccorrelations import htc_pinfin
from HHFtools.checks import check_validated
from HHFtools.pressuredrop import dynamic_pressure, friction_factor, pressure_loss

if __name__ == '__main__':
    import HHFtools
