import os 
import math
import sys
import attr
from tools import DHadTable
import modes 

sys.stdout.write('Loading syserr_818ipbv12.2 ...')
## ----------------------------------------------------------
##  Systematic  Errors
## ----------------------------------------------------------

tabdir = '818ipbv12'
tabfile = os.path.join(attr.cbxtabpath, tabdir,
                       'mode_dependent_syst.txt')
sys.stdout.write('from %s ...' % tabfile)
tab = DHadTable(tabfile)
tab.data_trim(factor=0.01)

sys_err_by_mode = {
    0: {'ST Background modeling': float(tab.cell_get('Bkgd shape', 'Kpi')),
        'Lepton veto'           : float(tab.cell_get('Lepton veto', 'Kpi'))
        },
    1: {'ST Background modeling': float(tab.cell_get('Bkgd shape', 'Kpipi0'))
        },
    3: {'ST Background modeling':  float(tab.cell_get('Bkgd shape', 'K3pi'))
        },
    200: {'ST Background modeling':  float(tab.cell_get('Bkgd shape', 'Kpipi'))
          },
    201: {'ST Background modeling':  float(tab.cell_get('Bkgd shape', 'Kpipipi0'))
          },
    202: {'ST Background modeling': float(tab.cell_get('Bkgd shape', 'Kspi'))
          },
    203: {'ST Background modeling': float(tab.cell_get('Bkgd shape', 'Kspipi0'))
          },
    204: {'ST Background modeling': float(tab.cell_get('Bkgd shape', 'Ks3pi'))
          },
    205: {'ST Background modeling': float(tab.cell_get('Bkgd shape', 'KKpi'))
          }}



sys_err = {
    'Detector simulation' : {
        'tracks':
        { 'fractional uncertainty' : 0  , 'correction factor' : 1        },
        'charged pions' :                                       
        { 'fractional uncertainty' : 0.0025 , 'correction factor' : 0.995    },
        'charged kaons' :                                       
        { 'fractional uncertainty' : 0.003,   'correction factor' : 0.99},
        'electrons'  :                                          
        { 'fractional uncertainty' : 0.     , 'correction factor' : 1        },
        'showers'  :                                            
        { 'fractional uncertainty' : 0.     , 'correction factor' : 1        },
        'K0S' :                                                 
        { 'fractional uncertainty' : float(tab.cell_get('KS0', 'Kspi'))  ,
          'correction factor' : 1},
        'pi0' :                                                 
        { 'fractional uncertainty' : 0.015   , 'correction factor' : 0.939 },
        'eta' :                                                 
        { 'fractional uncertainty' : 0.     , 'correction factor' : 1        }
        
        }, 

    'Fit parameter uncertainty': {
        'ND0D0Bar'    :  [0] ,
        'BrD2KPi'     : [ float(tab.cell_get('Delta E (*)', 'Kpi'))
                          ],
    
        'BrD2KPiPi0'  : [ float(tab.cell_get('Delta E (*)', 'Kpipi0')),
                          float(tab.cell_get('Substructure (*)', 'Kpipi0')),
                          float(tab.cell_get('Mult. cand. (*)', 'Kpipi0'))
                          ],    

        'BrD2KPiPiPi' : [ float(tab.cell_get('Delta E (*)', 'K3pi')),
                          float(tab.cell_get('Substructure (*)', 'K3pi')),
                          float(tab.cell_get('Mult. cand. (*)', 'K3pi'))
                          ],
    
        'ND+D-'       : [0] ,
        
        'BrD2KPiPi'   : [ float(tab.cell_get('Delta E (*)', 'Kpipi')),
                          float(tab.cell_get('Substructure (*)', 'Kpipi')),
                          float(tab.cell_get('Mult. cand. (*)', 'Kpipi'))
                          ],

        
        'BrD2KPiPiPi0': [ float(tab.cell_get('Delta E (*)', 'Kpipipi0')),
                          float(tab.cell_get('Substructure (*)', 'Kpipipi0')),
                          float(tab.cell_get('Mult. cand. (*)', 'Kpipipi0'))
                          ],

    
        'BrD2KsPi'    : [ float(tab.cell_get('Delta E (*)', 'Kspi')),
                          float(tab.cell_get('Mult. cand. (*)', 'Kspi'))
                          ],

        
        'BrD2KsPiPi0' : [ float(tab.cell_get('Delta E (*)', 'Kspipi0')),
                          float(tab.cell_get('Substructure (*)', 'Kspipi0')),
                          float(tab.cell_get('Mult. cand. (*)', 'Kspipi0'))
                          ],

        
        'BrD2KsPiPiPi': [ float(tab.cell_get('Delta E (*)', 'Ks3pi')),
                          float(tab.cell_get('Substructure (*)', 'Ks3pi')),
                          float(tab.cell_get('Mult. cand. (*)', 'Ks3pi'))
                          ],

    
        'BrD2KKPi'    : [ float(tab.cell_get('Delta E (*)', 'KKpi')),
                          float(tab.cell_get('Substructure (*)', 'KKpi')),
                          float(tab.cell_get('Mult. cand. (*)', 'KKpi'))
                          ]

        },
    
    'Fractional uncertainty per yield'       : 0,
    'Fractional uncertainty per D'           : 0,
    
    'Fractional uncertainty per D associated with fit parameter':{
        'ND0D0Bar'    : 0 ,
        'BrD2KPi'     : float(tab.cell_get('FSR', 'Kpi')),
        'BrD2KPiPi0'  : float(tab.cell_get('FSR', 'Kpipi0')),
        'BrD2KPiPiPi' :  float(tab.cell_get('FSR', 'K3pi')),
        'ND+D-'       : 0 ,                   
        'BrD2KPiPi'   : float(tab.cell_get('FSR', 'Kpipi')),
        'BrD2KPiPiPi0': float(tab.cell_get('FSR', 'Kpipipi0')),
        'BrD2KsPi'    : float(tab.cell_get('FSR', 'Kspi')),
        'BrD2KsPiPi0' : float(tab.cell_get('FSR', 'Kspipi0')),
        'BrD2KsPiPiPi': float(tab.cell_get('FSR', 'Ks3pi')),
        'BrD2KKPi'    : float(tab.cell_get('FSR', 'KKpi'))
        },

    'Fractional uncertainty per single tag'  : 0,
    
    'Fractional uncertainty per single tag associated with fit parameter':{
        'ND0D0Bar'    : [0] ,
        'BrD2KPi'     : [ float(tab.cell_get('Tracking', 'Kpi')), 
                          float(tab.cell_get('Signal shape', 'Kpi')) ],

        'BrD2KPiPi0'  : [ float(tab.cell_get('Tracking', 'Kpipi0')), 
                          float(tab.cell_get('Signal shape', 'Kpipi0')) ],
        
        'BrD2KPiPiPi' :  [ float(tab.cell_get('Tracking', 'K3pi')), 
                          float(tab.cell_get('Signal shape', 'K3pi')) ],

        'ND+D-'       : [0] ,

        'BrD2KPiPi'   :  [ float(tab.cell_get('Tracking', 'Kpipi')), 
                          float(tab.cell_get('Signal shape', 'Kpipi')) ],

        'BrD2KPiPiPi0':  [ float(tab.cell_get('Tracking', 'Kpipipi0')), 
                          float(tab.cell_get('Signal shape', 'Kpipipi0')) ],

        'BrD2KsPi'    :  [ float(tab.cell_get('Tracking', 'Kspi')), 
                          float(tab.cell_get('Signal shape', 'Kspi')) ],

        'BrD2KsPiPi0' :  [ float(tab.cell_get('Tracking', 'Kspipi0')), 
                          float(tab.cell_get('Signal shape', 'Kspipi0')) ],

        'BrD2KsPiPiPi':  [ float(tab.cell_get('Tracking', 'Ks3pi')), 
                          float(tab.cell_get('Signal shape', 'Ks3pi')) ],

        'BrD2KKPi'    :  [ float(tab.cell_get('Tracking', 'KKpi')), 
                          float(tab.cell_get('Signal shape', 'KKpi')) ]
        },
    
    'Fractional uncertainty per double tag' : 0.002,
    
    # 'Double DCSD interference(Neutral DT)': 0.008, # No need in this version 
    'Final state radiation' : 0.005

    }

sys.stdout.write('OK. \n')

