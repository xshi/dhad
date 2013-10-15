global newconstants
set newconstants no

global dset
if { [info exists env(DATASET)] } {
    set dset $env(DATASET)
} else {
    set dset 31
}


default prompt off
if [ catch {
    exception continueEventLoop on
    exception status
    global env

    #load in the cleog command
    if { [info exists env(RANDOMSEEDS)] } {
	run_file $env(SCRIPTDIR)/cleog_command_local.tcl
    } else {
	run_file $env(C3_SCRIPTS)/cleog_command.tcl
    }

    #if our output file exist we want to delete it
    set fileout $env(OUTDIR)/cleog_$env(DECAYTITLE)_$env(BATCH).pds
    if { [ tcl_file exists $fileout ]==1 } {
	echo "deleting file '$fileout'"
	tcl_file delete $fileout
    }  
    
    if { $newconstants == "yes" } {
	cleog gen EvtGenProd $env(NUMEVT) out $fileout [join $run_command_line] \
	    -user_decay $env(UDECAY)  -post {	
		proc sel RunEventNumberProc ;
		run_file $env(C3_SCRIPTS)/exclude_constants_streams.tcl
		exclude_constants_streams drsimulation
		constants in /nfs/cleo3/constants/db/Codi standard CLEO3default streams drsimulation   
	    }
    } else {
	if { [ info exists env(RUNNUMBER) ] } {
	    cleog gen EvtGenProd $env(NUMEVT) out $fileout \
		run $env(RUNNUMBER) \
		-user_decay $env(UDECAY)  -post {	
		    proc sel RunEventNumberProc ;
		}
	} else {
	    cleog gen EvtGenProd $env(NUMEVT) out $fileout \
		dataset $dset -job $env(BATCH) \
		-user_decay $env(UDECAY)  -post {	
		    proc sel RunEventNumberProc ;
		}
	}
    }	
    
} catchMessage ] {
    puts $catchMessage
}

quit
