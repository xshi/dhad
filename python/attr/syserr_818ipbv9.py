import math
import sys
sys.stdout.write('Loading syserr_818ipbv9 ...')
## ----------------------------------------------------------
##  Systematic  Errors
## ----------------------------------------------------------
sys_err_by_mode = {
    0: {'ST Background modeling': 0.004, #0.0059, #0.004,
        'Lepton veto'           : 0.001,
        'Delta E requirement'   : 0.001, #0.005,
        'Signal lineshape'      : 0.0039, #0.0029,
        'FSR'                   : 0.008, #0.0089,
        'Multiple candidates'   : 0.0
        },
    1: {'ST Background modeling': 0.01,  #0.012, #0.010,
        'Trigger simulation'    : 0.0,   #0.002,
        'Delta E requirement'   : 0.002, #0.005,
        'Signal lineshape'      : 0.005, #0.0135,
        'Resonant substructure' : 0.0052, #0.003,
        'FSR'                   : 0.003,  #0.0034,
        'Multiple candidates'   : 0.008
        },
    3: {'ST Background modeling': 0.004, #0.0064,  #0.004,
        'Delta E requirement'   : 0.001,   #0.005,
        'Signal lineshape'      : 0.005,   #0.0079,
        'Resonant substructure' : 0.0121,  #0.012,
        'FSR'                   : 0.006,   #0.0079,
        'Multiple candidates'   : 0.0
        },
    200: {'ST Background modeling': 0.0041, #0.004,
          'Delta E requirement'   : 0.002,  #0.005,
          'Signal lineshape'      : 0.0033, #0.0032,
          'Resonant substructure' : 0.0052, #0.006,
          'FSR'                   : 0.005,  #0.0071,
          'Multiple candidates'   : 0.0
          },
    201: {'ST Background modeling': 0.01, # 0.0331, #0.015,
          'Delta E requirement'   : 0.002,  #0.005,
          'Signal lineshape'      : 0.0049, #0.0133,
          'Resonant substructure' : 0.0091, #0.005,
          'FSR'                   : 0.002,  #0.0031,
          'Multiple candidates'   : 0.005
          },
    202: {'ST Background modeling': 0.003, #0.0091, #0.004,
          'Trigger simulation'    : 0.0,    #0.001,
          'Delta E requirement'   : 0.001,  #0.005,
          'Signal lineshape'      : 0.004,  #0.0036,
          'FSR'                   : 0.004,  #0.0054,
          'Multiple candidates'   : 0.002
          },
    203: {'ST Background modeling': 0.01,  #0.0146,  #0.010,
          'Delta E requirement'   : 0.005,  #0.010,
          'Signal lineshape'      : 0.0047, #0.0049,
          'Resonant substructure' : 0.0078, #0.012,
          'FSR'                   : 0.002,  #0.0011,
          'Multiple candidates'   : 0.0
          },
    204: {'ST Background modeling': 0.01,  # 0.0124, #0.010,
          'Delta E requirement'   : 0.010,  #0.005,
          'Signal lineshape'      : 0.0055, #0.0063,
          'Resonant substructure' : 0.0061, #0.005,
          'FSR'                   : 0.005,  #0.0058,
          'Multiple candidates'   : 0.0
          },
    205: {'ST Background modeling': 0.0080, #0.010,
          'Delta E requirement'   : 0.002,  #0.010,
          'Signal lineshape'      : 0.0055, #0.0060,
          'Resonant substructure' : 0.0185, #0.013,
          'FSR'                   : 0.003,  #0.0033,
          'Multiple candidates'   : 0.002
          }}


sys_err = {
    'Detector simulation' : {
    'tracks':
    { 'fractional uncertainty' : 0.003  , 'correction factor' : 1        },
    'charged pions' :                                       
    { 'fractional uncertainty' : 0.0025 , 'correction factor' : 0.995    },
    'charged kaons' :                                       
    { 'fractional uncertainty' : 0.003, #math.sqrt(0.003**2+0.006**2),
      'correction factor' : 0.99},
    'electrons'  :                                          
    { 'fractional uncertainty' : 0.     , 'correction factor' : 1        },
    'showers'  :                                            
    { 'fractional uncertainty' : 0.     , 'correction factor' : 1        },
    'K0S' :                                                 
#    { 'fractional uncertainty' : 0.018  , 'correction factor' : 1        },
    { 'fractional uncertainty' : 0.018  , 'correction factor' : 1.00859933},
    'pi0' :                                                 
        #    { 'fractional uncertainty' : 0.02   , 'correction factor' : 0.961    },
        { 'fractional uncertainty' : 0.015   , 'correction factor' : 0.939 },
    'eta' :                                                 
    { 'fractional uncertainty' : 0.     , 'correction factor' : 1        }

    }, 

    'Fit parameter uncertainty': {
    'ND0D0Bar'    :  [0] ,
    'BrD2KPi'     : [sys_err_by_mode[0]['Delta E requirement']],
                     
    'BrD2KPiPi0'  : [sys_err_by_mode[1]['Delta E requirement'],
                     sys_err_by_mode[1]['Trigger simulation'],
                     sys_err_by_mode[1]['Resonant substructure'],
                     sys_err_by_mode[1]['Multiple candidates']],
    
    'BrD2KPiPiPi' : [sys_err_by_mode[3]['Delta E requirement'],
                     sys_err_by_mode[3]['Resonant substructure'],
                     sys_err_by_mode[3]['Multiple candidates']],

    'ND+D-'       : [0] ,

    'BrD2KPiPi'   : [sys_err_by_mode[200]['Delta E requirement'],
                     sys_err_by_mode[200]['Resonant substructure'],
                     sys_err_by_mode[200]['Multiple candidates']],

    
    'BrD2KPiPiPi0': [sys_err_by_mode[201]['Delta E requirement'],
                     sys_err_by_mode[201]['Resonant substructure'],
                     sys_err_by_mode[201]['Multiple candidates']],

    
    'BrD2KsPi'    : [sys_err_by_mode[202]['Delta E requirement'],
                     sys_err_by_mode[202]['Trigger simulation'],
                     sys_err_by_mode[202]['Multiple candidates']],

    
    'BrD2KsPiPi0' : [sys_err_by_mode[203]['Delta E requirement'],
                     sys_err_by_mode[203]['Resonant substructure'],
                     sys_err_by_mode[203]['Multiple candidates']],

    
    'BrD2KsPiPiPi': [sys_err_by_mode[204]['Delta E requirement'],
                     sys_err_by_mode[204]['Resonant substructure'],
                     sys_err_by_mode[204]['Multiple candidates']],

    
    'BrD2KKPi'    : [sys_err_by_mode[205]['Delta E requirement'],
                     sys_err_by_mode[205]['Resonant substructure'],
                     sys_err_by_mode[205]['Multiple candidates']]
    },
    
    'Fractional uncertainty per yield'       : 0,
    'Fractional uncertainty per D'           : 0,

    'Fractional uncertainty per D associated with fit parameter':{
    'ND0D0Bar'    : 0 ,
    'BrD2KPi'     : sys_err_by_mode[0]['FSR'],
    'BrD2KPiPi0'  : sys_err_by_mode[1]['FSR'],
    'BrD2KPiPiPi' : sys_err_by_mode[3]['FSR'],
    'ND+D-'       : 0 ,                   
    'BrD2KPiPi'   : sys_err_by_mode[200]['FSR'],
    'BrD2KPiPiPi0': sys_err_by_mode[201]['FSR'],
    'BrD2KsPi'    : sys_err_by_mode[202]['FSR'],
    'BrD2KsPiPi0' : sys_err_by_mode[203]['FSR'],
    'BrD2KsPiPiPi': sys_err_by_mode[204]['FSR'],
    'BrD2KKPi'    : sys_err_by_mode[205]['FSR']
    },

    'Fractional uncertainty per single tag'  : 0,

    'Fractional uncertainty per single tag associated with fit parameter':{
    'ND0D0Bar'    : 0 ,
    'BrD2KPi'     : sys_err_by_mode[0]['Signal lineshape'],
    'BrD2KPiPi0'  : sys_err_by_mode[1]['Signal lineshape'],
    'BrD2KPiPiPi' : sys_err_by_mode[3]['Signal lineshape'],
    'ND+D-'       : 0 ,
    'BrD2KPiPi'   : sys_err_by_mode[200]['Signal lineshape'],
    'BrD2KPiPiPi0': sys_err_by_mode[201]['Signal lineshape'],
    'BrD2KsPi'    : sys_err_by_mode[202]['Signal lineshape'],
    'BrD2KsPiPi0' : sys_err_by_mode[203]['Signal lineshape'],
    'BrD2KsPiPiPi': sys_err_by_mode[204]['Signal lineshape'],
    'BrD2KKPi'    : sys_err_by_mode[205]['Signal lineshape']
    },

    'Fractional uncertainty per double tag' : 0.002,

    #'Double DCSD interference(Neutral DT)': 0.008,
    'Double DCSD interference(Neutral DT)': 0.002,
    'Final state radiation' : 0.005
    
    }

sys.stdout.write('OK. \n')
