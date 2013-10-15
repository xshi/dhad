if { ( $env(INPUTDATA) == "USERLOCALMC" ) } {
#    set skim no
    set skim yes
    set oldskim no
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    run_file $env(FILELIST)
}

if { ( $env(INPUTDATA) == "USERLOCALDATA" ) } {
    set skim no
    set oldskim no
    set preliminaryPass2 no
    set millionMC no
    set mc no
    run_file $env(FILELIST)
}

if { ( $env(INPUTDATA) == "USERLOCALDATAFILTER" ) } {
    set skim no
    set oldskim no
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set dtagfilter yes
    run_file $env(FILELIST)
}

if { ( $env(INPUTDATA) == "data31_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data31
}

if { ( $env(INPUTDATA) == "data32_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data32
}

if { ( $env(INPUTDATA) == "data32_1_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 202126 202900
}


if { ( $env(INPUTDATA) == "data32_2_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs  202901 203082
}




if { ( $env(INPUTDATA) == "data33_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data33
}



if { ( $env(INPUTDATA) == "data35_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data35
}

if { ( $env(INPUTDATA) == "data36_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data36
}

if { ( $env(INPUTDATA) == "data37_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data37
}

if { ( $env(INPUTDATA) == "data37_1_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 208067 209420
}

if { ( $env(INPUTDATA) == "data37_2_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 209421 209967
}

if { ( $env(INPUTDATA) == "data43_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data43
}

if { ( $env(INPUTDATA) == "data43_1_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 220898 222600
}

if { ( $env(INPUTDATA) == "data43_2_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 222601 223271
}


if { ( $env(INPUTDATA) == "data44_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data44
}


if { ( $env(INPUTDATA) == "data44_1_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 223279 224500
}

if { ( $env(INPUTDATA) == "data44_2_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 224501 225600
}

if { ( $env(INPUTDATA) == "data44_3_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 225601 226042
}


if { ( $env(INPUTDATA) == "data45_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data45
}

if { ( $env(INPUTDATA) == "data45_1_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 226429 227800
}

if { ( $env(INPUTDATA) == "data45_2_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs  227801 228271
}


if { ( $env(INPUTDATA) == "data46_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all dataset data46
}


if { ( $env(INPUTDATA) == "data46_1_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 228285 229300
}


if { ( $env(INPUTDATA) == "data46_2_dskim_evtstore" ) } {
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc no
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070822 dtag all runs 229301 230130
}


if { ( $env(INPUTDATA) == "USERLOCALMC_SKIMMED" ) } {
    set skim yes
    set oldskim no
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    run_file $env(FILELIST)
}

if { ( $env(INPUTDATA) == "USERLOCALDATA_SKIMMED" ) } {
    set skim yes
    set oldskim no
    set preliminaryPass2 no
    set millionMC no
    set mc no
    run_file $env(FILELIST)
}


if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_10xlumi_data31" ) } {
    echo "Inside the generic_mc-ddbar-dskim_10xlumi_data31"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070713 mc-ddbar-dskim 10xlumi dataset data31
}


if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_10xlumi_data32" ) } {
    echo "Inside the generic_mc-ddbar-dskim_10xlumi_data32"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070713 mc-ddbar-dskim 10xlumi dataset data32
}



if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_10xlumi_data33" ) } {
    echo "Inside the generic_mc-ddbar-dskim_10xlumi_data33"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070713 mc-ddbar-dskim 10xlumi dataset data33
}



if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_10xlumi_data35" ) } {
    echo "Inside the generic_mc-ddbar-dskim_10xlumi_data35"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070713 mc-ddbar-dskim 10xlumi dataset data35
}


if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_10xlumi_data36" ) } {
    echo "Inside the generic_mc-ddbar-dskim_10xlumi_data36"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070713 mc-ddbar-dskim 10xlumi dataset data36
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_10xlumi_data37" ) } {
    echo "Inside the generic_mc-ddbar-dskim_10xlumi_data37"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20070713 mc-ddbar-dskim 10xlumi dataset data37
}


if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data31" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data31"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim  dataset data31
}


if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data32" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data32"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim  dataset data32
}



if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data33" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data33"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim  dataset data33
}



if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data35" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data35"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim  dataset data35
}


if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data36" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data36"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim  dataset data36
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data37" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data37"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim dataset data37
}


if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data43"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim dataset data43
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data44"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim dataset data44
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data45"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim dataset data45
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46" ) } {
    echo "Inside the generic_mc-ddbar-dskim_20xlumi_data46"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-ddbar-dskim dataset data46
}

# Continuum generic MC


if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data31" ) } {
    echo "Inside the generic_mc-cont-dskim_5xlumi_data31"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-cont-dskim  dataset data31
}


if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data32" ) } {
    echo "Inside the generic_mc-cont-dskim_5xlumi_data32"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-cont-dskim  dataset data32
}



if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data33" ) } {
    echo "Inside the generic_mc-cont-dskim_5xlumi_data33"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-cont-dskim  dataset data33
}



if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data35" ) } {
    echo "Inside the generic_mc-cont-dskim_5xlumi_data35"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-cont-dskim  dataset data35
}


if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data36" ) } {
    echo "Inside the generic_mc-cont-dskim_5xlumi_data36"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-cont-dskim  dataset data36
}

if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data37" ) } {
    echo "Inside the generic_mc-cont-dskim_5xlumi_data37"
    set skim yes
    set preliminaryPass2 no
    set millionMC no
    set mc yes
    set use_setup_analysis yes
    module sel EventStoreModule
    eventstore in 20080728 mc-cont-dskim dataset data37
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_1" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 220898 221134 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_2" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 221135 221371 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_3" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 221372 221608 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_4" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 221609 221845 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_5" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 221846 222082 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_6" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 222083 222319 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_7" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 222320 222556 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_8" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 222557 222793 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_9" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 222794 223030 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data43_10_10" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 223031 223271 
}



if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_1" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 223279 223416 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_2" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 223417 223554 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_3" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 223555 223692 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_4" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 223693 223830 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_5" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 223831 223968 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_6" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 223969 224106 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_7" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 224107 224244 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_8" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 224245 224382 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_9" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 224383 224520 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_10" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 224521 224658 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_11" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 224659 224796 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_12" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 224797 224934 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_13" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 224935 225072 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_14" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 225073 225210 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_15" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 225211 225348 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_16" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 225349 225486 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_17" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 225487 225624 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_18" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 225625 225762 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_19" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 225763 225900 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data44_20_20" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 225901 226042 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_1" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 226429 226612 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_2" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 226613 226796 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_3" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 226797 226980 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_4" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 226981 227164 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_5" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 227165 227348 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_6" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 227349 227532 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_7" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 227533 227716 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_8" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 227717 227900 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_9" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 227901 228084 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data45_10_10" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 228085 228271 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_1" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 228285 228407 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_2" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 228408 228530 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_3" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 228531 228653 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_4" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 228654 228776 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_5" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 228777 228899 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_6" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 228900 229022 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_7" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 229023 229145 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_8" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 229146 229268 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_9" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 229269 229391 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_10" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 229392 229514 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_11" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 229515 229637 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_12" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 229638 229760 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_13" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 229761 229883 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_14" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 229884 230006 
}

if { ( $env(INPUTDATA) == "generic_mc-ddbar-dskim_20xlumi_data46_15_15" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-ddbar-dskim  runs 230007 230130 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data31" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data31 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data32" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data32 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data33" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data33 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data35" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data35 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data36" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data36 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data37" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data37 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data31" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data31 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data32" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data32 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data33" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data33 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data35" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data35 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data36" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data36 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data37" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data37 
}

if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data43" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-cont-dskim  dataset data43 
}

if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data44" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-cont-dskim  dataset data44 
}

if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data45" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-cont-dskim  dataset data45 
}

if { ( $env(INPUTDATA) == "generic_mc-cont-dskim_5xlumi_data46" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-cont-dskim  dataset data46 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data43" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data43 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data44" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data44 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data45" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data45 
}

if { ( $env(INPUTDATA) == "generic_mc-tau-dskim_5xlumi_data46" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-tau-dskim  dataset data46 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data43" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data43 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data44" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data44 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data45" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data45 
}

if { ( $env(INPUTDATA) == "generic_mc-radret-dskim_5xlumi_data46" ) } {
set skim yes 
set preliminaryPass2 no 
set millionMC no 
set mc yes 
set use_setup_analysis yes 
module sel EventStoreModule 
eventstore in 20080728 mc-radret-dskim  dataset data46 
}

