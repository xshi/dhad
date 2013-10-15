default prompt off
global env
exception continueEventLoop on
exception status

set fileout $env(OUTDIR)/pass2_$env(DECAYTITLE)_$env(BATCH).pds
if { [ tcl_file exists $fileout ]==1 } {
    echo "deleting file '$fileout'"
    tcl_file delete $fileout
}

set histout /home/xs32/work/CLEO/analysis/DHad/test/hist$env(BATCH).rzn

   run_file $env(C3_SCRIPTS)/mcpass2_command.tcl

   module sel LoadGeantModule
   module sel LoadHbookModule
   module sel HbookHistogramModule
   hbook file $histout
   hbook init

   mcpass2 file $env(INDIR)/cleog_$env(DECAYTITLE)_$env(BATCH).pds out $fileout -post {
   }
#   tcl_file delete $env(INDIR)/cleog_$env(DECAYTITLE)_$env(BATCH).pds

exit
    
