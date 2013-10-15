#
# This script sets the DSkimming parameters
# for DTagging
# load kaon selector
prod sel TagDKaonProd
 param TagDKaonProd pMax 2.0
 param TagDKaonProd pMin 0.05
# load pion slector
prod sel TagDPionProd
 param TagDPionProd pMax 2.0
 param TagDPionProd pMin 0.05
# load pi0 selector and set cuts 
prod sel TagDPi0Prod
 param TagDPi0Prod PullMass 3.0
 param TagDPi0Prod NumberSigmasMax 1000.
 param TagDPi0Prod RejectECPi0 false
# load eta selector and set cuts 
prod sel TagDEtaProd
 param TagDEtaProd PullMass 3.0
 param TagDEtaProd NumberSigmasMax 1000.
 param TagDEtaProd RejectECEta false
#  load kshort selector and set cuts 
prod sel TagDKShortProd
 param TagDKShortProd NumberMassSigmaCut 3.0
#
prod sel DTagProd
param DTagProd Kaons "TagDKaon"
param DTagProd Pions "TagDPion"
param DTagProd Pi0s  "TagDPi0"
param DTagProd Etas  "TagDEta"
param DTagProd Kshorts "TagDKShort"
#param DTagProd BCM_Cut $env(DSMassWin)
#param DTagProd DE_Cut $env(DSEWin)
# Default DSKim cuts:  DSMassWin (1.83/1.80 On/Below Res) DSEWin (.1)
