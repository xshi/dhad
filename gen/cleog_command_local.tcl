
#============================================================
# File: cleog_command_local.tcl
#
# Purpose:
#   create a 'cleog' command used to configure and run MC
#
# 
#============================================================

module sel EnableFPEModule

#--------------------------------------------------
# master procedure that calls all other procedures
#--------------------------------------------------
tcl_proc cleog args {
   # dynamically determine the subcommand to call
   #  this allows for easy addition of new subcommands
   #  (i.e. they just need to be called sub_<subcommand name>
   set generationType [lindex $args 0]
   if { 0 != [string compare sub_$generationType [namespace inscope cleog_ns info procs sub_$generationType] ] } {
      error "cleog: unknown sub command: $generationType"
   }
   eval cleog_ns::sub_$generationType [lrange $args 1 [llength $args] ]
   return
}

namespace eval cleog_ns {
# default location for random trigger files
variable default_merge_file_dir /nfs/cleoc/mc1/RandomTriggerEvents/Links

variable dataSet_run_list { 
#format:
# dataset <first run> <last run>
#{3 104100 107913}
#{4 107914 109688}
{5 109762 110278}
{6 110904 112258}
{7 112259 113214}
{8 113243 114137}
{9 114138 115063}
{10 115099 116093}
{11 116128 117105}
{12 117159 118166}
{13 118193 119022}
{14 119033 119927}
{16 121339 122178}
{17 122245 123304}
{18 123369 124548}
{19 124625 125416}
{20 125428 126204}
{21 126252 127545}
{22 127588 128401}
{23 128760 129221}
{24 129257 129488}
{25 129535 129865}
{26 129897 130187}
{27 130198 130630}
{28 130676 131640}
{29 131679 132285}
{30 132286 200977}
{31 200978 202101}
{32 202126 203082}
{33 203104 203634}
{34 203912 204348}
{35 205079 206185}
{36 206359 208047}
{37 208067 209967}
{38 211265 213069}
{39 213653 214863}
{40 215307 217385}
{41 217687 219721}
{42 219739 220729}
{43 220898 223271}
{44 223279 226042}
{45 226429 228271} 
{46 228285 230130} 
{47 230474 232255} 
}

variable dataset_mcconstants_script {
    {1 {cleo3 3}}
    {30 {cleoc 6}}
}

#--------------------------------------------------
# standard subcommands
#--------------------------------------------------
::proc sub_help {} {
   puts "\nDescription: cleog"
   puts "\n      generate monte carlo files"
   puts "\n  Subcommands are:"
   puts "     help   this page\n"
   puts "cleog file <mc particle file> out <out file> \[-nevents <#>\] \[-nomerge\] "
   puts "          \[ -post <commands>\] \[-user_decay <file>\] \[-standard_decay <file>\]"
   puts "          \[ -noconstants \]"
   puts "    starting from a file containing the decay particles <mc particle file> write" 
   puts "    out the mc file to <out file>."
   puts "    Can optionally choose to only process only some of the events in the file by"
   puts "    using \"-nevents <#>\"."
   puts ""
   puts "cleog gen <generator to use> <nevents> out <out file>  dataset <#> \[-job <#>\]"
   puts "           \[-start_event <#>\] \[-nomerge\] \[-post <commands>\]"
   puts "           \[-user_decay <file>\] \[-standard_decay <file>\]"
   puts "           \[-noconstants\]"
   puts "cleog gen <generator to use> <nevents> out <out file>  run <#>"
   puts "           \[-start_event <#>\] \[-nomerge\] \[-post <commands>\]"
   puts "           \[-user_decay <file>\] \[-standard_decay <file>\]"
   puts "           \[-noconstants\]"
   puts "   use the generator producer <generator to use> to <nevents> events and write"
   puts "   out the mc file to <out file>.  The option -start_event allows you to"
   puts "   start generation at an event number other than 1"
   puts "   The two forms differ by the way you specify what run number to use: "
   puts "   First form"
   puts "    specify the dataset number (e.g. 8).  The script then picks a run number"
   puts "    appropriate for that dataset.  Use the -job option to advance the run number"
   puts "    to something other than the default for that dataset"
   puts "   Second form"
   puts "    Specify the exact run number to be used."
   puts ""
   puts "  generation commands have the following standard options"
   puts "       -nomerge                do not run merge"
   puts "       -noconstants            do not load any constants. This allows"
   puts "                               you to explicitly setup the constants"
   puts "                               yourself"
   puts "       -user_decay <file>      specify a user decay .dec file"
   puts "       -standard_decay <file>  override standard decay.dec file"
   puts "       -post <commands>        tcl commands to issue after the mc"
   puts "                               job has been configured but before"
   puts "                               doing \"go\".  This should be used to"
   puts "                               specify a filter Processor: e.g."
   puts "                                -post \{proc sel MyFilterProc\}"
}

#setup MC generation using a file containing the QQ information
::proc sub_file args {
   variable standard_arg_names
   if { 3 > [llength $args] } {
      error "cleog: too few arguments"
   }
   set fileName [lindex $args 0]
   
   #add additional option to allow users to specify number of events to process
   set arg_names [concat { {-nevents 1} } $standard_arg_names]
   set parsedArgs [::suez::parse_args [lrange $args 1 [llength $args]] $arg_names ]
   
   set run_dataSet [determine_run_dataSet_from_file $fileName]

   # Set this to be _not_ 'EvtGenProd' to get the right MCInfoDelivery
   set argsArray(generatorProd) QQ

   # parse time stamp and assign it to emptysource
   set uTime [determine_timeStamp_from_file $fileName]

   # set bunchfinding flag setting to post processing command so that users
   # post processing commands could alter it.
   set rpExtension .rp
   if { 0 == [string compare $rpExtension [string range $fileName end-[expr [string length $rpExtension] -1] end] ] } {

       puts stdout "++++++++                               +++++++++"
       puts stdout "Forcing zero time offset for TrackletBunchFinder"
       puts stdout "++++++++                               +++++++++"

       array set argsArray $parsedArgs
       if [catch {
	   set argsArray(-post) [linsert $argsArray(-post) 0 "param TrackletBunchFinder ForceTimeOffset true; param TrackletBunchFinder TheForcedTimeOffset 0.0;prod desel MCSymmetricBeamProd;prod desel CesrBeamEnergyProd;source_format desel BeamSpotFileSourceFormat;"]
       } ] {
	   set argsArray(-post) "param TrackletBunchFinder ForceTimeOffset true; param TrackletBunchFinder TheForcedTimeOffset 0.0;prod desel MCSymmetricBeamProd;prod desel CesrBeamEnergyProd;source_format desel BeamSpotFileSourceFormat;"
       }
       set parsedArgs [array get argsArray]
   }

   setup_job $parsedArgs "set dummyVar \"$run_dataSet\""

   ::suez::load_proper_format $fileName
   ::suez::file in $fileName beginrun startrun event endrun physics
   
   if [ catch {
      array set argArray $parsedArgs
      set nevents $argArray(-nevents)
   } ] {
      set nevents -1
   }
   
   puts [::suez::prod lss]
   puts [::suez::proc lss]
   puts [::suez::source list]

   run_job $nevents [lindex $run_dataSet 0] $uTime
}

#use a generator Producer to generate the MC
::proc sub_gen args {
   variable standard_arg_names
   if { 5 > [llength $args] } {
      error "cleog: too few arguments"
   }
   set generatorProd [lindex $args 0]
   set nevents [lindex $args 1]
   
   switch [lindex $args 4] {
      dataset {
         set arg_names [concat { {dataset 1} {-job 1} {-start_event 1}} $standard_arg_names]
      }
      run { 
         set arg_names [concat { {run 1} {-start_event 1}} $standard_arg_names]
      }
      default { error "cleog: unknown sixth argument [lindex $args 5].  Should be \"dataset\" or \"run\""}
   }
   
   #add additional option to allow users to specify number of events to process
   set parsedArgs [::suez::parse_args [lrange $args 2 [llength $args]] $arg_names ]
   array set argsArray $parsedArgs
   
   switch [lindex $args 4] {
      dataset {
         set dataSet $argsArray(dataset)
         if { 0 != [llength [array get argsArray "-job"] ] } {
            set job $argsArray(-job)
         } else {
            set job 0
         }
         set runNumber [determine_run_from_dataSet $dataSet $job]
      }
      run {
         set runNumber $argsArray(run)
         set dataSet [determine_dataSet_from_run $runNumber]
      }
   }
   set argsArray(generatorProd) $generatorProd

   #add generatorProd to post processing command so that users
   # post processing commands could alter the behavior of this producer
   if [catch {
      set argsArray(-post) [linsert $argsArray(-post) 0 "::suez::prod sel $generatorProd;"]
   } ] {
      set argsArray(-post) "::suez::prod sel $generatorProd"
   }
   set parsedArgs [array get argsArray]
   setup_job $parsedArgs "list $runNumber $dataSet"

   #now check to see if the user has loaded any Processors
   # if they have, then we need to specify the number of events to process
   #  if not, then we can just let the source handle it
   ::suez::module sel MCSourceModule
   set start_event 1
   catch {
      set start_event $argsArray(-start_event)
   }
   
   #ignore any procs we know that are not filters
   set nonFilterProcs {RunEventNumberProc MCRunEvtNumberProc}
   set procList [::suez::loader_lss proc]
   foreach noFilterProc $nonFilterProcs {
      if {-1 != [set index [lsearch -exact $procList $noFilterProc] ] } {
           set procList [lreplace $procList $index $index] 
      }
   }
   if { 0 < [llength $procList] } {
      set genEvents [expr int(pow(2,30))]
      set runEvents $nevents
   } else {
      set genEvents $nevents
      set runEvents -1
   }
   ::suez::mcsource in MC $runNumber $genEvents $start_event

#puts [emptysource def givePhysics physics]
#puts [source act givePhysics physics]
   
   puts [::suez::prod lss]
   puts [::suez::proc lss]
   puts [::suez::source list]
   
   # set time to initial value and pass it to emptysource
   # mcsource will generate appropriate number and suez will
   # synchronize to it.
   set uTime 0
   
   run_job $runEvents $runNumber $uTime
}

#--------------------------------------------------
# handle the various parts of the job
#--------------------------------------------------

::proc setup_job {argArrayAsList getRun_RunSetCommand} {
  global env
  array set argArray $argArrayAsList
 
   #build a stack of commands we should issue to setup the job
   #  we do this rather than directly calling the commands so
   #  that any initial calculations we need to do to get all the
   #  data necessary to setup the job will not interfere with 
   #  the actual job setup
   set commandStack []
  
   lappend commandStack "setup_mcproperties [get_generator_name $argArray(generatorProd)]"

   #lappend commandStack "cleog_setup"
   
   if { 0 == [llength [array get argArray "-noconstants" ] ] } {
       lappend commandStack "setup_mcconstants [eval $getRun_RunSetCommand]"
   }
   if { 0 == [llength [array get argArray "-nomerge"] ] } {
       lappend commandStack "setup_merge [eval $getRun_RunSetCommand]"
   } else {
       lappend commandStack "setup [eval $getRun_RunSetCommand]"
   }

   if { 0 == [string compare $argArray(generatorProd) "EvtGenProd" ] } {
       lappend commandStack "::suez::prod sel EvtGenProd"
       lappend commandStack "::suez::param EvtGenProd decayFile $env(C3_DATA)/DECAY.DEC"
       lappend commandStack "::suez::param EvtGenProd evtpdl $env(C3_DATA)/evt.pdl"
   }


   if { 0 != [llength [array get argArray "-user_decay"] ] } {
       set generatorType [get_generator_name $argArray(generatorProd)]
       lappend commandStack "optional_user_decay_$generatorType $argArray(-user_decay)"
   }

   if { 0 != [llength [array get argArray "-standard_decay"] ] } {
       set generatorType [get_generator_name $argArray(generatorProd)]
       lappend commandStack "optional_standard_decay_$generatorType $argArray(-standard_decay)"
   }
   
   lappend commandStack "out_file $argArray(out)"

   if { 0 != [llength [array get argArray "-post"] ] } {
       lappend commandStack "namespace eval ::suez \{ [join $argArray(-post) ] \} "
   }
   
   #now issue the commands
   foreach command $commandStack {
       eval $command
   }
}


#run this procedure at the end of the job
::proc run_job {{nevents -1} {runNumber -1} {uTime 0}} {
   if {$nevents >= 0 } {
      ::suez::proc sel StopAfterNEventsProc
      ::suez::param StopAfterNEventsProc numberOfEvents $nevents
   }
   ::suez::go
   if {$nevents >= 0 } {
      #make sure their are no sources delivering beginruns, startruns or events
      ::suez::source clear
     
      #use this number to create endrun
      ::suez::emptysource one EndRun $runNumber [expr int( pow(2,31)-1)] -time $uTime endrun

      #need a dummy source of other streams
      ::suez::emptysource one Dummy [incr runNumber] 0 -time $uTime beginrun startrun event physics

      ::suez::go 1 endrun
      ::suez::source clear
   }
}


#--------------------------------------------------
# procedures used to handle the various optoins
#--------------------------------------------------

::proc setup_mcproperties { generator } {
   global env

    if { 0 == [string compare $generator "EvtGen"] } {
	::suez::prod sel MCInfoDeliveryEvtGenProd
	::suez::param MCInfoDeliveryEvtGenProd transTable $env(C3_DATA)/trans.tab
    } else {
	::suez::prod sel MCInfoDelivery
    }   
}

::proc setup {runNumber dataSet } {
   global env
   variable dataset_mcconstants_script

   #::suez::run_file $env(C3_SCRIPTS)/cleog.tcl
   ::suez::run_file $env(SCRIPTDIR)/cleog.tcl
   
    #find the appropriate constant script to call
    set detConfig ""
    foreach entry $dataset_mcconstants_script {
	set presentDataSet [lindex $entry 0]
	if { $dataSet == $presentDataSet } {
	    set conArg [lindex $entry 1]
	    set detConfig [lindex $conArg 0]
	    break
	}
	if {$dataSet > $presentDataSet} {
	    set conArg [lindex $entry 1]
	    set detConfig [lindex $conArg 0]
	} else {
	    break;
	}
    }
    if {$detConfig == ""} {
	error "no detector configuation specified"
    }

    if { $detConfig == "cleo3" } {
	::suez::run_file $env(C3_SCRIPTS)/cleo3MCSettings.tcl
    }
}

::proc setup_mcconstants {runNumber dataSet} {
    global env
    variable setup_constants_called
    variable dataset_mcconstants_script
    
    #find the appropriate constant script to call
    set constants_args ""
    foreach entry $dataset_mcconstants_script {
	set presentDataSet [lindex $entry 0]
	if { $dataSet == $presentDataSet } {
	    set constants_args [lindex $entry 1]
	    break
	}
	if {$dataSet > $presentDataSet} {
	    set constants_args [lindex $entry 1]
	} else {
	    break;
	}
    }
    if {$constants_args == ""} {
	error "can not find appropriate mc constants script for data set $dataSet"
    }
    eval "::suez::setup_constants cleog [lindex $constants_args 0] [lindex $constants_args 1]"
}

::proc setup_merge {runNumber dataSet} {
    global env 
    variable default_merge_file_dir
    variable setup_constants_called

    setup $runNumber $dataSet
    ::suez::run_file $env(C3_SCRIPTS)/cleog_merge.tcl
   
   #build file chain used for merging
   if [ catch {
      set mergFileDir $env(C3_MERGE_DIR)
      }
   ] {
      set mergFileDir $default_merge_file_dir
   }

   #create two lists: one with all files for runs less than we want
   # the other for run equal to or greater than that one.
   #Merge the two list so that the files are in order of 'closeness' to 
   # the run we want
   set fileList [glob $mergFileDir/data$dataSet/RandomTriggerEvents_*.pds]
   set lesserList []
   set greaterList []
   set ignoreBefore [string length "$mergFileDir/data$dataSet/RandomTriggerEvents_"]
   
   foreach file $fileList {
      if {[ string range $file $ignoreBefore end-4] < $runNumber} {
         lappend lesserList $file
      } else {
         lappend greaterList $file
      }  
   }

   #NOTE: this assumes that all files have the same length runNumbers
   set greaterList [lsort $greaterList]
   set reverseLesserList [lsort -decreasing $lesserList]
   
   if { [llength $lesserList] < [llength $greaterList] } {
      set shorterList $reverseLesserList
      set longerList $greaterList
   } else {
      set shorterList $greaterList
      set longerList $reverseLesserList
   }
   
   set totalList []
   for { set index 0 } { $index < [llength $shorterList]} {incr index} {
      lappend totalList [lindex $greaterList $index]
      lappend totalList [lindex $reverseLesserList $index]
   }
   
   for { set index [llength $shorterList]} {$index < [llength $longerList]} {incr index} {
      lappend totalList [lindex $longerList $index]
   }


   if { $dataSet < 30 } {
       ::suez::param CorrectedSVStripProd  production_tag PreMerge
       ::suez::prod sel SiMergeProd
       ::suez::prod sel ZDMergeProd
       ::suez::prod desel ZDMergeProd
   }

   ::suez::param SubFrameProd {

       if { $dataSet < 30 } {
	   ::suez::prod sel CorrectedSVStripProd
	   ::suez::prod sel SiGeom
	   ::suez::prod sel SiHitsProd
	   ::suez::prod sel ASiStorePro
	   ::suez::prod desel CalibratedZDHitProd
	   ::suez::prod desel ZDDriftFunctionProd
	   ::suez::prod desel ZDGeomProd
	   ::suez::prod desel ZDWireLayerProd
	   ::suez::prod desel AZDGeomProd
       }

       if [namespace inscope ::suez info exists setup_constants_called] {
	   namespace inscope ::suez unset setup_constants_called
       }
       setup_mcconstants $runNumber $dataSet

       ::suez::source_format sel PDSSourceFormat
       ::suez::source create randomTriggerChain
       foreach file $totalList {
	   ::suez::file add randomTriggerChain $file beginrun startrun event
       }
   }
}

::proc optional_standard_decay_QQ {decay} {
   ::suez::param MCInfoDelivery standardDecayDec $decay
}
::proc optional_user_decay_QQ {decay} {
    ::suez::param MCInfoDelivery userDecayDec $decay
}

::proc optional_standard_decay_EvtGen {decay} {
   ::suez::param EvtGenProd decayFile $decay
}
::proc optional_user_decay_EvtGen {decay} {
   ::suez::param  EvtGenProd udecayFile $decay
}

::proc optional_post {post_command} {
   eval $post_command
}

::proc out_file {filename } {
    global env
    ::suez::load_proper_sink_format $filename
    ::suez::file out $filename beginrun startrun "event [::suez::mc_output_cleog]" endrun physics
}

#--------------------------------------------------
# helper procedures
#--------------------------------------------------

::proc get_generator_name {generatorProd} {

    if { 0 == [string compare $generatorProd "EvtGenProd"] } {
	return "EvtGen"
    }

    return "QQ"
    
}




#list of standard arguments used by all 'cleog *' commands
variable standard_arg_names { {out 1} {-nomerge 0} {-noconstants 0} {-post 1} {-user_decay 1} {-standard_decay 1}}

::proc determine_dataSet_from_run {run} {
   variable dataSet_run_list
   if { $run < [lindex [lindex $dataSet_run_list 0] 1] } {
      error "cleog: run $run is before CLEO III physics data taking began"
   }
   
   foreach dataSet_run $dataSet_run_list {
      if { $run >= [lindex $dataSet_run 1] } {
         if {  (0 == [lindex $dataSet_run 2]) || ($run <= [lindex $dataSet_run 2]) } {
               return [lindex $dataSet_run 0]
         }
      }
      if { $run < [lindex $dataSet_run 1] } {
         error "cleog: run $run falls between dataset [expr [lindex $dataSet_run 0] - 1] and [lindex $dataSet_run 0]"
      }
   }
   return 1
}

::proc determine_run_from_dataSet {dataSet job} {
   global env 
   variable default_merge_file_dir
   
   #build file chain used for merging
   if [ catch {
      set mergeFileDir $env(C3_MERGE_DIR)
      }
   ] {
      set mergeFileDir $default_merge_file_dir
   }

   #create a list of the random trigger runs and use these
   # for the runs for the dataset
   set fileList [glob $mergeFileDir/data$dataSet/RandomTriggerEvents_*.pds]
   set runList []
   set ignoreBefore [string length "$mergeFileDir/data$dataSet/RandomTriggerEvents_"]
   
   foreach file $fileList {
      lappend runList [ string range $file $ignoreBefore end-4]
   }
   
   set runList [lsort -dictionary $runList]

   #start our lists from the center of the list and work our way outward
   if {1 == [expr [llength $runList] % 2] } {
       lreplace runList end end
   }
   
   set beginList []
   set endList []
   set halfwayIndex [expr [llength $runList]/2]
   for { set index 0} {$index < $halfwayIndex} {incr index} {
      lappend beginList [lindex $runList $index]
      lappend endList [lindex $runList [expr $halfwayIndex + $index] ]
   }
   set beginList [lsort -dictionary -decreasing $beginList]
   
   set runList []
   for { set index 0} {$index < $halfwayIndex} {incr index} {
      lappend runList [lindex $beginList $index]
      lappend runList [lindex $endList $index]
   }
   return [lindex $runList [expr $job%$halfwayIndex]]
}

::proc set_runNumber_from_record {rn} {
    variable runNumber
    set runNumber $rn
}
::proc determine_run_dataSet_from_file {fileName} {
   variable runNumber
   ::suez::load_proper_format $fileName
   
   set fileToken [::suez::file in $fileName beginrun]
   ::suez::proc sel DataInteractProc
    
   ::suez::param DataInteractProc auto_execute \{::suez::cleog_ns::set_runNumber_from_record \[ ::suez::record syncvalue beginrun\]\}
   ::suez::param DataInteractProc stop_stream beginrun
   ::suez::source activate $fileToken beginrun
   ::suez::go 1 beginrun
   ::suez::proc desel DataInteractProc
   ::suez::source remove $fileToken
   #temp
   #set runNumber "run/event/time=114000/0/10101"
   set runNumber [ lindex [ split [lindex [split $runNumber "="] 1 ] "/"] 0]
   return "$runNumber [determine_dataSet_from_run $runNumber]"
}

::proc set_timeStamp_from_record {rn} {
    variable timeStamp
    set timeStamp $rn
}

::proc determine_timeStamp_from_file {fileName} {
   variable timeStamp
   ::suez::load_proper_format $fileName

   set fileToken [::suez::file in $fileName beginrun]
   ::suez::proc sel DataInteractProc
   ::suez::param DataInteractProc auto_execute \{::suez::cleog_ns::set_timeStamp_from_record \[::suez::record syncvalue beginrun\]\}
   ::suez::param DataInteractProc stop_stream beginrun
   ::suez::source activate $fileToken beginrun
   ::suez::go 1 beginrun
   ::suez::proc desel DataInteractProc
   ::suez::source remove $fileToken
   set timeStamp [ lindex [ split [lindex [split $timeStamp "="] 1 ] "/"] 2]
   return "$timeStamp"
} 
}
# ========================================
# Command "cleog" added.
#   Do "cleog help" for further details.
# ========================================

