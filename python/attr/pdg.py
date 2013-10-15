"""
Providing Attributes of PDG.

"""

import os
import hep.pdt

__author__ = "Xin Shi <xs32@cornell.edu>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2006-2010 Xin Shi"
__license__ = "GNU GPL"



particle_data = hep.pdt.loadPdtFile(os.path.join(os.environ['C3_DATA'], 'evt.pdl'))


pdgid_Dz = 421
pdgid_Dzb = -421
pdgid_Dp = 411
pdgid_Dm = -411
pdgid_Kp = 321
pdgid_Km = -321
pdgid_pip = 211
pdgid_pim = -211
pdgid_piz = 111
pdgid_KS = 310
pdgid_KL = 130
pdgid_eta = 221
pdgid_etaprime = 331
pdgid_omega = 223
pdgid_rhop = 213
pdgid_rhom = -213
pdgid_rhoz = 113
pdgid_gamma = 22
pdgid_ep = -11
pdgid_em = 11
pdgid_nue = 12
pdgid_nueb = -12
pdgid_mup = -13
pdgid_mum = 13
pdgid_numu = 14
pdgid_numub = -14
pdgid_jpsi = 443
pdgid_psiprime = 100443
pdgid_Dsp = particle_data['D_s+'].id
pdgid_Dsm = particle_data['D_s-'].id
pdgid_Dpstar = particle_data['D*+'].id
pdgid_Dmstar = particle_data['D*-'].id
pdgid_Dspstar = particle_data['D_s*+'].id
pdgid_Dsmstar = particle_data['D_s*-'].id
pdgid_phi = particle_data['phi'].id
pdgid_K0star = particle_data['K*0'].id
pdgid_K0bstar = particle_data['anti-K*0'].id
pdgid_K0star0 = particle_data['K_0*0'].id
pdgid_K0bstar0 = particle_data['anti-K_0*0'].id
pdgid_gammaFSR = 100022


interesting_particles = (pdgid_KS, pdgid_KL, pdgid_Kp, pdgid_Km,
                         pdgid_pip, pdgid_pim, pdgid_piz,
                         #pdgid_eta, pdgid_etaprime,
                         pdgid_ep, pdgid_em, pdgid_nue, pdgid_nueb,
                         pdgid_mup, pdgid_mum, pdgid_numu, pdgid_numub,
                         pdgid_gamma)
