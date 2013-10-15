# FILE: cleog.tcl
#
# Purpose: Tcl script to setup Cleog running under Suez.
#
#          Used by cleog_command 
#
########################################################################

# ------------------- tcl try-catch block to cause graceful abort if
#                     a module/proc/ducer cannot load
if [ catch {

   default prompt off

#--------------------- order matters in this next section -----------------

## Random Number Module - manages random number generator and initialize it
#  'randomInit' assures pseudorandom seeds based on time of day
   module sel RandomModule
   random seeds $env(RANDOMSEEDS) 0 
   random create
   #random randomInit
   
# This must be loaded before any other version of these commons
   module select ZebraCommonsModule

# producer below is needed for CollatedRawDRHits; gets overridden for other raw
   prod sel RawDataProd

# creates raw data objects from MCResponse for each sub-detector
   prod sel MCRawDataProd

#--------------------- order matters in the above section! ---------------

#     inject noise hits in Rich (set to false if merging random triggers later)
   param MCRawDataProd useRichFakeMerge true
#     scale noise up by a factor of 3 relatively to the initial model
   param MCRawDataProd useRichNoiseScaleFactor 3.0

## MCResponse 
#  Create MCResponse and MCDecayTree objects and trigger Cleog/Geant
   prod sel MCResponseProd
   param MCResponseProd PrintGeantBanks false

   prod sel DetectorConfigurationProd

#  Serve materials & media in geant3-mode
   prod sel Geant3MaterialsMediaProd
#  Set kinetic energy cuts to 1 MeV for hadrons and muons, instead of 10 MeV
   param Geant3MaterialsMediaProd useLowKineticEnergyCuts true


#  Detector Geometry producers - passive and active
   prod sel IRGeomProd
   prod sel DRGeom
   prod sel DRWireLayerProd
   prod sel ADRGeomProd
   prod sel CcGeomProd
   prod sel RichGeom
   prod sel CoilGeomProd
   prod sel MUGeomProd
   prod sel ZDGeomProd            
   prod sel ZDWireLayerProd        
   prod sel AZDGeomProd           

#  Magnetic field
   prod sel MagFieldProd

# for calibration information
   prod sel C3ccConProd
   prod sel CDOffCal
   prod sel ZDDriftFunctionProd

## For trigger
## create CcEnergyHits/CalibratedDRHits for the CC/DR trigger part:
   prod sel C3ccReconProd
   prod sel CalibratedDRHitProd
   prod sel PreliminaryDRHitProd

   prod sel TrackletBunchFinder
#	param TrackletBunchFinder ForceTimeOffset true
#	param TrackletBunchFinder TheForcedTimeOffset 0.0

# these are for remaining calibrated hit tables for other detectors
   prod sel DRCACorrectHitProd
   prod sel CorrectedSVStripProd
   prod sel RichCalibratedHits
   prod sel MuonCalibratedHitProd
   prod sel CalibratedZDHitProd

# load mu constants producer
    prod select MuConsProd

   #cleo3 beamspot access
   run_file $env(C3_SCRIPTS)/BeamSpot.tcl

   prod sel MCTriggerPhaseProd
# ponyisi 2004-09-21: disable trigger phase smearing until simulation better
# understood
#   param MCTriggerPhaseProd triggerPhaseWidth 0.5

   prod sel MCSymmetricBeamProd
# bkh 02/05/04: allow energy spread from constants
# bkh 12/09/03: set parameters for low energy running
#   use x size in beamspot object (it will get reduced by measured y size in quadrature)
    param MCSymmetricBeamProd BeamSpotMenu useXSizeParam false
#   use fixed y size which is close to true CESR size in y
    param MCSymmetricBeamProd BeamSpotMenu useYSizeParam true
    param MCSymmetricBeamProd BeamSpotMenu ySize         0.0000045
#   use z size in beamspot object
    param MCSymmetricBeamProd BeamSpotMenu useZSizeParam false
#   use actual measured center of beam in beamspot object, not default to zero
    param MCSymmetricBeamProd BeamSpotMenu useZeroCenter false

   prod sel CesrBeamEnergyProd

   prod sel DBRunHeaderProd
   prod sel DBEventHeaderProd

    prod sel TriggerDataProd
    prod sel TriggerL1DataProd

    prod sel TriggerPhaseForMCProd

# prints random # seed for each event
   proc sel MCRunEvtNumberProc

} resultString ] { # ------------------- tcl try-catch block
    puts stderr "cleog source/modules **not** ok"
    puts stderr "resultString:"
    puts stderr "$resultString"
    exit
} else {
    puts stdout "Loading ok"
    puts stdout "resultString:"
    puts stdout "$resultString"
}



#######################################################
# CVS Info
# $Id$
#
# $Log$
# Revision 1.1  2010/10/03 15:06:46  xs32
# add for this task
#
# Revision 1.76  2004/09/23 17:53:31  ponyisi
# disable trigger phase smearing until simulation better understood
#
# Revision 1.75  2004/03/24 17:33:00  bkh
# cleog/mcpass2 script changes for cleoc/cleo3 MC
#
# Revision 1.74  2004/03/02 22:00:03  cdj
# cleog now handles detector configuration based constants differences
#
# Revision 1.73  2004/02/05 16:36:48  bkh
# Remove explicit setting of beam energy spread...now handled by constants system
#
# Revision 1.72  2003/12/18 17:17:07  bkh
# Additions to get MuonCalibratedHit objects merged and in pass2, mcpass2 output
#
# Revision 1.71  2003/12/11 22:36:07  bkh
# In cleog.tcl, make low kinetic energy cutoff default; put high kinetic energy cutoff setting in cleogMCSettings.tcl
#
# Revision 1.70  2003/12/10 15:49:07  bkh
# Fix typo in new parameter setting in cleog.tcl
#
# Revision 1.69  2003/12/09 21:44:08  bkh
# Alter cleog.tcl defaults to use CLEOc beam spot & beam energy spread
#
# Revision 1.68  2003/12/05 19:48:06  jed
#  Add in ZDDriftFunctionProd
#
# Revision 1.67  2003/10/14 00:57:27  ryd
# Changes to allow using EvtGen
#
# Revision 1.66  2003/04/16 18:10:03  bkh
# cleog.tcl: add ZD producer calls
# merge.tcl: add DetectorConfigurationProd selection
# controlMCWriteout_cleog.tcl: add zd objects to list to write out
#
# Revision 1.65  2002/09/27 20:41:17  bkh
# Add DetectorConfigurationProd to cleog and tracking to prepare for ZD era
#
# Revision 1.64  2002/09/10 16:10:27  bkh
# Change beam spot center back to 0,0,0 at least until discussed formally
#
# Revision 1.63  2002/09/09 19:19:54  bkh
# Add muon processor to analysis_output_command to assure storage helper
# selected
# Modify cleog tcl files to use BeamSpot now and new parameters
#
# Revision 1.62  2002/05/13 18:32:17  bkh
# Modify for new QQDriverDelivery
#
# Revision 1.61  2002/04/04 15:40:45  bkh
# Alter for accomodation of trigger phase producers
#
# Revision 1.60  2002/03/26 18:44:53  mahlke
# added CesrBeamEnergyProd (MCSymmetricBeamProd needs this now)
#
# Revision 1.59  2002/02/21 18:11:50  bkh
# Use pass2_3 constants not newest
#
# Revision 1.58  2002/02/08 21:44:46  bkh
# New mcpass2 commands and other mods
#
# Revision 1.57  2002/02/07 22:20:29  bkh
# Make work for physics streams
#
# Revision 1.56  2002/02/06 23:19:52  bkh
# Fix ups
#
# Revision 1.55  2002/02/05 22:43:22  bkh
# Update scripts
#
# Revision 1.54  2002/01/31 20:30:24  cdj
# modified cleog scripts to work with new cleog command
#
# Revision 1.53  2001/12/18 22:46:09  bkh
# cleog now supplies corrected hits objects
#
# Revision 1.52  2001/11/30 22:12:32  ts
# scale noise in RICH up by a factor of 3
#
# Revision 1.51  2001/11/21 16:48:02  bkh
# Storage helper for raw data no longer needed; it is built into RawData
#
# Revision 1.50  2001/11/07 18:39:27  mahlke
# updated usage info
#
# Revision 1.49  2001/10/12 18:50:04  cdj
# -can now write out endruns
# -no longer requests FFREAD input by default
# -update how to use documention
#
# Revision 1.48  2001/09/26 21:24:58  mahlke
# add C3ccReconProd for CC trigger sim
#
# Revision 1.47  2001/09/21 21:30:50  bkh
# Move access to ascii mc cc constants to proper place
#
# Revision 1.46  2001/09/21 16:40:55  bkh
# Add reading in of ascii constants in cleog.tcl until
# libraries come up to speed.
#
# Revision 1.45  2001/07/20 18:38:46  bkh
# Added RawDataStorageHelper, commented out Ascii an AsciiTest Sink formats
#
# Revision 1.44  2001/07/20 18:27:43  bkh
# Add selection of PDSSinkFormat
#
# Revision 1.43  2001/07/08 19:14:21  cdj
# added producers needed by trigger simulation
#
# Revision 1.42  2001/03/15 22:29:06  bkh
# Add selection of MagFieldProd
#
# Revision 1.41  2001/02/16 23:47:26  ts
# get Rich geometry from database
#
# Revision 1.40  2001/02/14 14:02:40  lkg
# added a new getMCConstants.tcl that will get ALL constants for MC generation
# jobs.  Modified cleog.tcl to use the new getMCConstants.tcl
#
# Revision 1.39  2000/07/01 23:29:21  lkg
# * made file sourceable => remove all input files, output files, go's, exits...
# * converted script to run from the constants database
# * added sample usage in comments at file header
#
# Revision 1.38  2000/06/30 13:46:33  cdj
# cleog.tcl now includes DRCAPedestal constants
#
# Revision 1.37  2000/06/02 01:56:13  lkg
# add try-catch block to catch problems loading modules/sources
#
# Revision 1.36  2000/05/22 17:07:57  jjo
# Update for new FFREAD and Geant batch mode.
# Currenlty use old behavior.  Will change when update
# is known to work.
#
# Revision 1.35  2000/05/18 22:34:49  cdj
# modified cleog.tcl to use the new ascii constants needed for CDOffCal which are obtained from CDOffCalFileConstants.tcl
#
# Revision 1.34  2000/05/16 18:57:17  bkh
# Add C3ccConProd to both scripts
#
# Revision 1.33  2000/05/08 14:28:57  jjo
# Remove code to deal with QQ & beginruns which wasn't needed
# and caused errors in logfile.
#
# Revision 1.32  2000/05/05 15:38:26  jjo
# Add MCRunEvtNumberProc to print random # seeds every event
#
# Revision 1.31  2000/05/05 13:12:02  jjo
# Add back changes from versions 1.21-1.29
#
# Revision 1.30  2000/04/21 17:22:00  pg
# Modified cleog.tcl to deal with DR aligned geometry
#
# Revision 1.29  2000/04/19 14:46:43  jjo
# Remove emptysoure that creates beginrun - not
# needed as QQ rp file creates the beginrun.
#
# Revision 1.28  2000/04/18 21:57:42  jjo
# Fix typo of 'source summary' to 'source status'
#
# Revision 1.27  2000/04/18 21:06:31  jjo
# Change run number to 104000 to correspond to a real
# engineering data run #
#
# Revision 1.26  2000/04/18 18:53:27  jjo
# Change emptysource to use run # 100000 instead of 75001
#
# Revision 1.25  2000/04/18 18:40:35  jjo
# Change to QQ file with run number 100,000
# and use C3ccEngineeringFileConstants.tcl
#
# Revision 1.24  2000/04/17 21:52:08  jjo
# Comment out endruns - we can't currently create them
#
# Revision 1.23  2000/04/17 17:12:28  jjo
# Output asc file instead of calling ExtractMCProc to
# trigger the MC generation.
#
# Revision 1.22  2000/04/12 22:15:39  jjo
# Change to write output ascii file
#
# Revision 1.21  2000/04/10 15:20:29  bkh
# remove C3ccReconProd
#
# Revision 1.20  2000/03/21 17:50:21  bkh
# Add C3ccReconProd
#
# Revision 1.19  2000/01/31 17:03:41  lkg
# Updated to access MCParticleProperties via the MCInfoProducer producer,
# and to get generator-level information from an MCDecayTree provided
# by QQDriverDelivery.  The shortcomings of roar in the latter lead to
# some awful kludges, which will disappear once QQ is running in suez.
#
# Revision 1.18  1999/12/15 18:56:35  bkh
# Replace MaterialProd and G3iMaterialsMediaProd with Geant3MaterialsMediaProd
#
# Revision 1.17  1999/12/14 00:32:18  jjo
# Added ASiStorePro producer, Increase NEVENT to 100.
# Improved organization & comments.
#
# Revision 1.16  1999/11/09 22:30:07  jjo
# Add constants file for ADRGeom
#
# Revision 1.15  1999/10/29 20:51:25  bkh
# Include muon geometry and newly names wire layer producer
#
# Revision 1.14  1999/10/27 23:09:55  jjo
# Reorganize, put SV & Rich constants into seperate tcl files
#
# Revision 1.13  1999/10/26 19:35:14  jjo
# Change to use DR3AsciiConstants.tcl to read DR constants
#
# Revision 1.12  1999/10/25 17:01:27  bkh
# Added RandomModule commands, CC constants access, remove histogram termination
#
# Revision 1.11  1999/10/20 22:39:03  jjo
# Add SV & DR  constants & calls for DR response simulation
#
# Revision 1.10  1999/09/22 16:53:44  bkh
# Changed producer name for MCRawDataProd
#
# Revision 1.9  1999/09/22 16:48:29  bkh
# update producer names for G3iMaterialsMediaProd and MaterialProd
#
# Revision 1.8  1999/09/09 19:10:26  jjo
# Only cosmetic changes - improve comments, add suez summary
#
#
