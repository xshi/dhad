default prompt off
exception continueEventLoop on
report level info

source_format sel PDSSourceFormat

file in $env(INDIR)/pass2_$env(DECAYTITLE)_$env(BATCH).pds
setup_dtag standard 

dtag_output fileout $env(OUTDIR)/dskim_$env(DECAYTITLE)_$env(BATCH).pds mc
setup_analysis

go

#tcl_file delete $env(INDIR)/pass2_$env(DECAYTITLE)_$env(BATCH).pds
exit
