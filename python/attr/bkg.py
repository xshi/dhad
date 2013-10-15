"""
Providing Attributes of Backgrounds for BF fitter

"""

__author__ = "Xin Shi <xs32@cornell.edu>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2006-2010 Xin Shi"
__license__ = "GNU GPL"

#efficiencies and uncertainties for signal
efficiencies_single = {
    '0':   .650, #.662,
    '1':   .352, #.356,
    '3':   .464, #.469,
    '200': .546, #.552,
    '201': .281, #.283,
    '202': .456, #.454,
    '203': .240, #.244,
    '204': .323, #.318,
    '205': .470  #.470
    }

efficiencies_single_uc = {
    '0':   .001, #.003,
    '1':   .001, #.001,
    '3':   .001, #.002,
    '200': .001, #.002,
    '201': .001, #.002,
    '202': .001, #.004,
    '203': .001, #.002,
    '204': .001, #.002,
    '205': .002  #.004
    }

#efficiencies and uncertainties for background [generic]
bkg_efficiencies_single = {
    'kpi': .663,
    'kpipi0': .356,
    'k3pi': .470,
    'kkspi': 0.128,
    'kkspibar': 0.128,
    'k3pigam': 0.00415,
    '3pi': 1,
    '3pipi0': 1,
    '5pi': 1,
    'kskspi': 0.013,
    'ks3pigam': 0.00445 }

bkg_efficiencies_single_uc = {
    'kpi': .005,
    'kpipi0': .012,
    'k3pi': .010,
    'kkspi': .004,
    'kkspibar': .004,
    'k3pigam': 0.0007,
    '3pi': 0,
    '3pipi0': 0,
    '5pi': 0,
    'kskspi': .001,
    'ks3pigam': 0.0008 }

pdg_bf = {
    '0': 0.0389,
    '1': 0.139,
    '3': 0.0809,
    '200': 0.094,
    '201': 0.0608,
    '202': 0.0149,
    '203': 0.0690,
    '204': 0.0310,
    '205': 0.0098 }

#BF for background modes

bkg_pdg_bf = {
    'kpi': 1.48e-4,
    'kpipi0': 3.05e-4,
    'k3pi': 2.62e-4,
    'kkspi': 3.5e-3,
    'kkspibar': 2.6e-3,
    'kskspi': 1.6e-2,
    '3pi': 81,
    '3pipi0': 188,
    '5pi': 117
    }


bkg_pdg_bf_uc = {
    'kpi': 0.07e-4,
    'kpipi0': 0.17e-4,
    'k3pi': 0.21e-4,
    'kkspi': 0.5e-3,
    'kkspibar': 0.5e-3,
    'kskspi': 0.7e-2,
    '3pi': 21.7,
    '3pipi0': 55.7,
    '5pi': 79.4
    }


dcsd_pdg_bf = { '0': bkg_pdg_bf['kpi'],
                '1': bkg_pdg_bf['kpipi0'],
                '3': bkg_pdg_bf['k3pi'] }

dcsd_efficiencies_single = { '0': bkg_efficiencies_single['kpi'],
                             '1': bkg_efficiencies_single['kpipi0'],
                             '3': bkg_efficiencies_single['k3pi'] }

# The following gives D0 -> KS K+ pi-
scsd_pdg_bf = { '3': bkg_pdg_bf['kkspibar'] }
scsd_efficiencies_single = { '3': bkg_efficiencies_single['kkspibar'] }


fake_mode_list = { 'kpi': '0', 'kpipi0': '1',  'kkspi': '3', 'kkspibar': '3',
                   '3pi': '202', '5pi': '204', 'kskspi': '204',
                   '3pipi0': '203', 'k3pi': '3',
                   }
fake_mode_order = [ 'kpi', 'kpipi0', 'k3pi', 'kkspi', 'kkspibar',
                    'd0generic',
                    '3pi', '3pipi0', '5pi', 'kskspi',
                    'dpgeneric' ]

single_tag_order = [ '0', '1', '3', '200', '201', '202', '203', '204', '205' ]




