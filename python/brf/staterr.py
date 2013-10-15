"""
Module for Branching Fractions Fitting 

"""
import os
import sys
import tools
import attr
import commands

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def data_fit_staterrors(fit, prefix, verbose=0):
    outfilename  = 'bf_stat'
    
    outfile  = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                              comname=outfilename)
    fdir = outfile.replace(outfilename, '')
    com1_name = 'newfit-cat_files_data_statonly.sh'

    #bashbase = os.path.join(attr.base, 'src', attr.src, 'brf')
    com1 = tools.set_file(extbase=attr.brfpath, prefix=prefix, comname=com1_name)
    sdir = com1.replace(com1_name, '')
    com2 = create_bash_statonly(fdir, sdir, com1)

    if fit or not os.access(outfile, os.F_OK) :
        print 'Running fitter for staterrors ...'
        run_bf_fitter(com2, outfile, verbose)
    
    start_line_str   = 'Fitted parameters'
    start_column_str = '+-'
    end_column_str   = '('
    end_line_str     = 'Difference from seeds'

    data = tools.get_column_from_file(outfile,
                                      start_line_str, start_column_str,
                                      end_column_str, end_line_str,
                                      verbose = verbose)
    datafilename =  'data_fit_staterrors'

    outfile  = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                              comname=datafilename)

    fo, bakfile = tools.backup_output(outfile)
    for line in data: fo.write('%s\n' %line)
    tools.check_output(fo, outfile, bakfile)

def create_bash_statonly(fdir, sdir, outfile):

    EXE=attr.fitter

    sys.stdout.write('Using fitter: %s \n' %EXE)

    bash_content = '''#!/usr/bin/env bash

EXE=%s
FDIR=%s
SDIR=%s

YLDFILE=$FDIR/statonly_data_yields_for_werner
BKGBRS=$FDIR/data_statonly_external_bkg_bfs_for_werner
BKGEFFS=$FDIR/data_bkg_effs_for_werner
BKGERRS=$FDIR/data_bkg_effs_errs_for_werner
SIGSINGEFFS=$FDIR/signal_single_efficiencies_for_werner
SIGSINGERRS=$FDIR/zero_single_efficiencies_errors_for_werner
SIGDOUBEFFS=$FDIR/signal_double_efficiencies_for_werner
SIGDOUBERRS=$FDIR/zero_double_efficiencies_errors_for_werner
SYSTERRORS=$FDIR/newfit-data_statonly_systerrors
SEEDS=$FDIR/data_seeds

echo "#!/usr/bin/env bash" > $SDIR/newfit-data_statonly.sh
echo "$EXE <<EOF" >> $SDIR/newfit-data_statonly.sh
echo -e "n\\nn" >> $SDIR/newfit-data_statonly.sh
cat $FDIR/newfit-modedef >> $SDIR/newfit-data_statonly.sh
cat $YLDFILE >> $SDIR/newfit-data_statonly.sh
cat $BKGBRS >> $SDIR/newfit-data_statonly.sh
cat $SIGSINGEFFS >> $SDIR/newfit-data_statonly.sh
cat $SIGDOUBEFFS >> $SDIR/newfit-data_statonly.sh
cat $BKGEFFS >> $SDIR/newfit-data_statonly.sh
cat $SIGSINGERRS >> $SDIR/newfit-data_statonly.sh
cat $SIGDOUBERRS >> $SDIR/newfit-data_statonly.sh
cat $BKGERRS >> $SDIR/newfit-data_statonly.sh
#echo -e "0\\n0\\n0\\n0\\n0\\n0\\n1\\n1\\n1\\n1\\n1\\n1" >> \
$SDIR/newfit-data_statonly.sh
cat $SYSTERRORS >> $SDIR/newfit-data_statonly.sh
cat $SEEDS >> $SDIR/newfit-data_statonly.sh
echo -e "n\\nn\\nn\\ny" >> $SDIR/newfit-data_statonly.sh
cat $FDIR/data_statonly_brratiodef >> $SDIR/newfit-data_statonly.sh
echo -e "\\ny" >> $SDIR/newfit-data_statonly.sh
cat $FDIR/data_statonly_crosssectionsdef >> $SDIR/newfit-data_statonly.sh
echo "EOF" >> $SDIR/newfit-data_statonly.sh
chmod +x $SDIR/newfit-data_statonly.sh
''' % (EXE, fdir, sdir)


    fo, bakfile = tools.backup_output(outfile)
    fo.write(bash_content)
    tools.check_output(fo, outfile, bakfile)
    bashfile = outfile
    os.chmod(bashfile, 0755)
    output = commands.getoutput(bashfile)
    if output:
        print 'Stop message from DHadBF:: create_bash_statonly:'
        print '-------------------------------------------------'
        print output
        print '-------------------------------------------------'
        sys.exit()

    new_bashfile = os.path.join(sdir, 'newfit-data_statonly.sh')

    return new_bashfile
   
def run_bf_fitter(com, outfile, verbose=0):
    fo, bakfile = tools.backup_output(outfile)
    output = commands.getoutput(com)
    if verbose > 0:
        print output
    fo.write(output)
    tools.check_output(fo, outfile, bakfile)

    
def generic_fit_staterrors(fit, prefix, verbose=0):
    outfilename  = 'bf_stat'
    
    outfile  = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                              comname=outfilename)
    fdir = outfile.replace(outfilename, '')

    com1_name = 'newfit-cat_files.sh'

    com1 = tools.set_file(extbase=attr.brfpath, prefix=prefix, comname=com1_name)
    sdir = com1.replace(com1_name, '')

    if '281ipbv0.0' in prefix or '281ipbv0.1' in prefix \
           or '281ipbv12.0' in prefix or '818ipbv12.0' in prefix:
        com2 = create_bash_generic_20060927(fdir, sdir, com1)
        
    else:
        com2 = create_bash_generic_20070611(fdir, sdir, com1)
    
    if fit: 
        print 'Running fitter for staterrors ...'
        run_bf_fitter(com2, outfile, verbose)

    
def create_bash_generic_20060927(fdir, sdir, outfile):
    EXE = attr.fitter.replace('20070611', '20060927')

    sys.stdout.write('Using fitter: %s \n' %EXE)

    bash_content = '''#!/usr/bin/env bash

EXE=%s
FDIR=%s
SDIR=%s

YLDFILE=$FDIR/generic_yields_for_werner
BKGBRS=$FDIR/generic_external_bkg_bfs_for_werner
BKGEFFS=$FDIR/generic_bkg_effs_for_werner
BKGERRS=$FDIR/generic_bkg_effs_errs_for_werner
SIGSINGEFFS=$FDIR/signal_single_efficiencies_for_werner
SIGSINGERRS=$FDIR/signal_single_efficiencies_errors_for_werner
SIGDOUBEFFS=$FDIR/signal_double_efficiencies_for_werner
SIGDOUBERRS=$FDIR/signal_double_efficiencies_errors_for_werner
SYSTERRORS=$FDIR/newfit-generic_systerrors
SEEDS=$FDIR/generic_seeds

echo "#!/usr/bin/env bash" > $SDIR/newfit-generic.sh
echo "$EXE <<EOF" >> $SDIR/newfit-generic.sh
echo -e "n\\nn" >> $SDIR/newfit-generic.sh
cat $FDIR/newfit-modedef >> $SDIR/newfit-generic.sh
cat $YLDFILE >> $SDIR/newfit-generic.sh
cat $BKGBRS >> $SDIR/newfit-generic.sh
cat $SIGSINGEFFS >> $SDIR/newfit-generic.sh
cat $SIGDOUBEFFS >> $SDIR/newfit-generic.sh
cat $BKGEFFS >> $SDIR/newfit-generic.sh
cat $SIGSINGERRS >> $SDIR/newfit-generic.sh
cat $SIGDOUBERRS >> $SDIR/newfit-generic.sh
cat $BKGERRS >> $SDIR/newfit-generic.sh
#echo -e "0\\n0\\n0\\n0\\n0\\n0\\n1\\n1\\n1\\n1\\n1\\n1" >> \
$SDIR/newfit-generic.sh
cat $SYSTERRORS >> $SDIR/newfit-generic.sh
cat $SEEDS >> $SDIR/newfit-generic.sh
echo -e "n\\nn\\nn\\ny" >> $SDIR/newfit-generic.sh
cat $FDIR/generic_statonly_brratiodef >> $SDIR/newfit-generic.sh
echo -e "n" >> $SDIR/newfit-generic.sh
echo "EOF" >> $SDIR/newfit-generic.sh
chmod +x $SDIR/newfit-generic.sh
''' % (EXE, fdir, sdir)


    fo, bakfile = tools.backup_output(outfile)
    fo.write(bash_content)
    tools.check_output(fo, outfile, bakfile)
    bashfile = outfile
    os.chmod(bashfile, 0755)
    output = commands.getoutput(bashfile)
    if output:
        raise ValueError(output)

    new_bashfile = os.path.join(sdir, 'newfit-generic.sh')

    return new_bashfile


def create_bash_generic_20070611(fdir, sdir, outfile):
    EXE = attr.fitter
    sys.stdout.write('Using fitter: %s \n' %EXE)
    bash_content = '''#!/usr/bin/env bash

EXE=%s
FDIR=%s
SDIR=%s

YLDFILE=$FDIR/generic_yields_for_werner
BKGBRS=$FDIR/generic_external_bkg_bfs_for_werner
BKGEFFS=$FDIR/generic_bkg_effs_for_werner
BKGERRS=$FDIR/generic_bkg_effs_errs_for_werner
SIGSINGEFFS=$FDIR/signal_single_efficiencies_for_werner
SIGSINGERRS=$FDIR/signal_single_efficiencies_errors_for_werner
SIGDOUBEFFS=$FDIR/signal_double_efficiencies_for_werner
SIGDOUBERRS=$FDIR/signal_double_efficiencies_errors_for_werner
SYSTERRORS=$FDIR/newfit-generic_systerrors
SEEDS=$FDIR/generic_seeds

echo "#!/usr/bin/env bash" > $SDIR/newfit-generic.sh
echo "$EXE <<EOF" >> $SDIR/newfit-generic.sh
echo -e "n\\nn" >> $SDIR/newfit-generic.sh
cat $FDIR/newfit-modedef >> $SDIR/newfit-generic.sh
cat $YLDFILE >> $SDIR/newfit-generic.sh
cat $BKGBRS >> $SDIR/newfit-generic.sh
cat $SIGSINGEFFS >> $SDIR/newfit-generic.sh
cat $SIGDOUBEFFS >> $SDIR/newfit-generic.sh
cat $BKGEFFS >> $SDIR/newfit-generic.sh
cat $SIGSINGERRS >> $SDIR/newfit-generic.sh
cat $SIGDOUBERRS >> $SDIR/newfit-generic.sh
cat $BKGERRS >> $SDIR/newfit-generic.sh
#echo -e "0\\n0\\n0\\n0\\n0\\n0\\n1\\n1\\n1\\n1\\n1\\n1" >> \
$SDIR/newfit-generic.sh
cat $SYSTERRORS >> $SDIR/newfit-generic.sh
cat $SEEDS >> $SDIR/newfit-generic.sh
echo -e "n\\nn\\nn\\ny" >> $SDIR/newfit-generic.sh
cat $FDIR/generic_statonly_brratiodef >> $SDIR/newfit-generic.sh
echo -e "\\ny" >> $SDIR/newfit-generic.sh
cat $FDIR/generic_statonly_crosssectionsdef >> $SDIR/newfit-generic.sh
echo "EOF" >> $SDIR/newfit-generic.sh
chmod +x $SDIR/newfit-generic.sh
''' % (EXE, fdir, sdir)


    fo, bakfile = tools.backup_output(outfile)
    fo.write(bash_content)
    tools.check_output(fo, outfile, bakfile)
    bashfile = outfile
    os.chmod(bashfile, 0755)
    output = commands.getoutput(bashfile)
    if output:
        raise ValueError(output)

    new_bashfile = os.path.join(sdir, 'newfit-generic.sh')

    return new_bashfile
