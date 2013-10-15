#
# Tcl will run the HadronicDNtupleProc to produce an ntuple
#
# Environment variables that control this script:
#
# INPUTDATA data sample to process
# OUTPUTDIR directory to write output to
# SUFFIX to be added to output name
#

default prompt off
#report level debug

global env
global preliminaryPass2
global millionMC
global skim
global mc
global dtagfilter
global use_setup_analysis

set oldskim no
set dtagfilter no
set use_setup_analysis no

run_file $env(USER_SRC)/HadronicDNtupleProc/Test/dataselection.tcl

if { [info exists env(USE_SETUP_ANALYSIS)] } {
    set use_setup_analysis yes
    if { [info exists env(ENERGY_FROM_RUNINFO)] } {
        #exclude_constants_streams {beamenergyshift}
        #constants in $env(C3_CONST) standard PostPASS2-C_5 streams beamenergyshift
        prod sel RunInfoProd
        run_file $env(C3_SCRIPTS)/RunInfo.tcl
    }
    if { [info exists env(ISTVAN_MC_FIX)] } {
	prod sel PhotonDecaysProd
	prod sel $env(USER_SHLIB)/MCBeamEnergyFromMCBeamParametersProd
	module sel CorbaModule
	corba init
	module sel RunStatisticsSourceModule
	runstatistics in
	prod sel LabNet4MomentumFromCrossingAngleProd
    }
}

echo "We have 'preliminaryPass2' set to: " $preliminaryPass2
echo "We have 'millionMC' set to: " $millionMC
echo "We have 'skim set' to: " $skim
echo "We have 'mc set' to: " $mc

if { $use_setup_analysis == "yes" } {
setup_analysis
} else {
run_file $env(C3_SCRIPTS)/runOnNewPass2.tcl
#run_file $env(C3_SCRIPTS)/runOnICHEP04Pass2.tcl

run_file $env(C3_SCRIPTS)/exclude_constants_streams.tcl

module sel RunStatisticsSourceModule
runstatistics in
prod sel LabNet4MomentumFromCrossingAngleProd
}
# Run Rochester EID
run_file $env(C3_CVSSRC)/EID/scripts/eid.tcl

if { $preliminaryPass2 == "yes" } {

    source rm runinfo
    file in $env(C3_INFO)/data/ri032204.runinfo
    source rm cchotlist
    file in $env(C3_INFO)/data/ch032204.cchotlist beginrun
    source rm ccrungain
    file in $env(C3_INFO)/data/cr032204.ccrungain beginrun

    set sourceList [source_stream_list]
    foreach sourceInList $sourceList {
	
	if { "Codi" == [lindex $sourceInList 0] } {
	    set streamInCodi [lindex $sourceInList 1]
	    break;
	}
    }
    lappend streamInCodi dedxkinematicfitused

    eval "source bind Codi $streamInCodi"
}

prod sel NavigationProd

module sel HbookHistogramModule
#hbook init
#module sel RootHistogramModule

#prod sel PhotonDecaysProd
#param PhotonDecaysProd Pi0Finding_Menu EnergyMin 0.030
#param PhotonDecaysProd Pi0Finding_Menu E925Scheme 2

if { $skim == "yes" && $use_setup_analysis == "no" } {
    # set photon decays prod not to reconstruct new pi0's
    prod desel PhotonDecaysProd
}

#prod sel DBRunHeaderProd

#prod sel DBEventHeaderProd
#prod sel TriggerL1DataProd

if { $skim == "no" } {
     run_file $env(USER_SRC)/HadronicDNtupleProc/Test/DTagDSkim.tcl

#param PhotonDecaysProd Pi0Finding_Menu E925Scheme 2

     param DTagProd BCM_Cut 1.83
     param DTagProd DE_Cut 0.1
}

if { $dtagfilter == "yes" } {
     proc sel DFilterProc
}

# Load PhotonDecaysProd for loose pi0's
prod sel PhotonDecaysProd production "loosePi0"
PhotonDecaysProd@loosePi0 Pi0Finding_Menu E925Scheme 0

proc sel SkipBadRunsProc

# Skip events which consum too much CPU time 
proc sel SkipBadEventsProc
param SkipBadEventsProc EventsToSkip $env(USER_SRC)/HadronicDNtupleProc/Test/EventsToSkip.txt


proc sel RunEventNumberProc
param RunEventNumberProc Frequency 500
prod sel DDoubleTagProd
prod sel VFinderQualityProd
prod sel TrkmanProd
prod sel TrkmanSelectionProd
proc sel HadronicDNtupleProc
#proc sel DoubTagTest
param HadronicDNtupleProc makeHbookNtuple false
param HadronicDNtupleProc makeRootNtuple true
if { ($env(INPUTDATA) != "USERLOCALMC") && \
     ($env(INPUTDATA) != "USERLOCALDATA") && \
     ($env(INPUTDATA) != "USERLOCALDATAFILTER") && \
     ($env(INPUTDATA) != "USERLOCALMC_SKIMMED")  && \
     ($env(INPUTDATA) != "USERLOCALDATA_SKIMMED")} {
param HadronicDNtupleProc rootFilename $env(OUTPUTDIR)/$env(INPUTDATA).root
param HadronicDNtupleProc hbookFilename $env(OUTPUTDIR)/$env(INPUTDATA).rzn
} else {
param HadronicDNtupleProc rootFilename $env(OUTPUTDIR)/$env(FNAME).root
}

if { $millionMC == "yes" } {
    source rm runinfo
    file in $env(C3_INFO)/mc/mmc.runinfo startrun beginrun
    source rm ccrungain
    file in $env(C3_INFO)/mc/mmc.ccrungain beginrun
    source rm cchotlist
    file in $env(C3_INFO)/mc/mmc.cchotlist beginrun
}

if { $mc == "yes" } {
    prod sel MCTagHolderProd
    param HadronicDNtupleProc makeMCblock true
}


if { [info exists env(SKIM_DATA)] } {
    echo "Using the DataSkim"
    if { ( $env(INPUTDATA) == "data31_dskim_evtstore" ) } {
	run_file $env(USER_SRC)/HadronicDNtupleProc/Test/DataSkim_data31.tcl
    }
    if { ( $env(INPUTDATA) == "data32_dskim_evtstore" ) } {
	run_file $env(USER_SRC)/HadronicDNtupleProc/Test/DataSkim_data32.tcl
    }
    if { ( $env(INPUTDATA) == "data33_dskim_evtstore" ) } {
	run_file $env(USER_SRC)/HadronicDNtupleProc/Test/DataSkim_data33.tcl
    }
    if { ( $env(INPUTDATA) == "data35_dskim_evtstore" ) } {
	run_file $env(USER_SRC)/HadronicDNtupleProc/Test/DataSkim_data35.tcl
    }
    if { ( $env(INPUTDATA) == "data36_dskim_evtstore" ) } {
	run_file $env(USER_SRC)/HadronicDNtupleProc/Test/DataSkim_data36.tcl
    }
    if { ( $env(INPUTDATA) == "data37_dskim_evtstore" ) } {
	run_file $env(USER_SRC)/HadronicDNtupleProc/Test/DataSkim_data37.tcl
    }
} else {
    source ls
    go 1
    source ls
    go
}


exit


















