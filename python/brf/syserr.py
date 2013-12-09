"""
Module for Branching Fractions Fitting 

"""
import os
import sys
import tools
import attr 
from tools import DHadTable
import commands
from attr.modes import modes
import math
from staterr import run_bf_fitter

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def get_statonly_sys_err(prefix='', verbose = 0):
    filename = 'newfit-data_statonly_systerrors'
    outfile  = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                              comname=filename)
    statonly_sys_err = get_statonly_sys_err_for_fit(prefix)
    statonly_sys_list = map(str, statonly_sys_err)
    content = '\n'.join(statonly_sys_list)+ '\n'
    fo, bakfile = tools.backup_output(outfile)
    fo.write(content)
    tools.check_output(fo, outfile, bakfile)


def get_statonly_sys_err_generic(prefix='', verbose = 0):
    filename = 'newfit-generic_systerrors'
    outfile  = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                              comname=filename)
    statonly_sys_err = get_statonly_sys_err_for_fit_generic(prefix)
    statonly_sys_list = map(str, statonly_sys_err)
    content = '\n'.join(statonly_sys_list)+ '\n'
    fo, bakfile = tools.backup_output(outfile)
    fo.write(content)
    tools.check_output(fo, outfile, bakfile)

def get_statonly_sys_err_for_fit(prefix):
    simulation_parts = attr.simulation_parts
    fit_paras  = attr.fit_paras

    label = prefix.replace('dir_', '')
    sys_err, m = attr.sys_err(label)

    list_ = []
    for name in ['fractional uncertainty', 'correction factor']:
        for item in simulation_parts:
            _value =  sys_err['Detector simulation'][item][name]
            if name == 'fractional uncertainty':
                _value = 0
            list_.append(_value)

    for fit_para in fit_paras:
        list_.append(0)

    list_.append(0)
    list_.append(0)

    for fit_para in fit_paras:
        list_.append(0)

    list_.append(0)

    for fit_para in fit_paras:
        list_.append(0)

    list_.append(0)

    return  list_

def get_statonly_sys_err_for_fit_generic(prefix):
    simulation_parts = attr.simulation_parts
    fit_paras  = attr.fit_paras

    label = prefix.replace('dir_', '')
    sys_err, m = attr.sys_err(label)

    list_ = []
    for name in ['fractional uncertainty', 'correction factor']:
        for item in simulation_parts:
            _value =  sys_err['Detector simulation'][item][name]
            if name == 'fractional uncertainty':
                _value = 0
            list_.append(_value)

    for fit_para in fit_paras:
        list_.append(0)

    list_.append(0)
    list_.append(0)
    list_.append(0)
    list_.append(0)

    if '281ipbv0' in prefix or '281ipbv12.0' in prefix \
           or '818ipbv12.0' in prefix:
        return  list_

    for fit_para in fit_paras:
        list_.append(0)
        list_.append(0)

    return list_


def get_sys_err(prefix= '' , opt_sys_err='', verbose=0):
    label = prefix.replace('dir_', '')

    filename = 'newfit-data_systerrors'
    outfile  = tools.set_file(
        extbase   = attr.brfpath, prefix  = prefix, 
        comname   = filename)

    sys_err_ = get_sys_err_for_fit(label)
    
    sys_list = map(str, sys_err_)
    content = '\n'.join(sys_list)+ '\n'
    fo, bakfile = tools.backup_output(outfile)

    fo.write(content)
    tools.check_output(fo, outfile, bakfile)

    
def get_sys_err_for_fit(label):
    simulation_parts = attr.simulation_parts
    fit_paras  = attr.fit_paras

    #line_shape_sys = get_signal_shape_sys(label)
    #fsr_sys = get_fsr_sys(label)
    
    #sys_err = attr.sys_err(label)
    sys_err, sys_err_by_mode = attr.sys_err(label)

    if label == '818ipbv7':
        n = 0    
        for mode in modes:
            n+= 1
            sig = float(line_shape_sys[n])*.01
            fsr = float(fsr_sys[n])*.01
            sys_err_by_mode[mode]['Signal lineshape'] = sig
            sys_err_by_mode[mode]['FSR'] = fsr

    # if label not in ['818ipbv12.2', '818ipbv12.3', '818ipbv12.4', '818ipbv12.5', 
    #                  '818ipbv12.6']:
    #     raise NameError(label)
    #     n = 0    
    #     for fit_para in fit_paras:
    #         if fit_para == 'ND0D0Bar' or fit_para =='ND+D-': continue
    #         n+= 1
    #         sig = float(line_shape_sys[n])*.01
    #         fsr = float(fsr_sys[n])*.01

    #         sys_err['Fractional uncertainty per single tag associated \
    #         with fit parameter'][fit_para]= sig
        
    #         sys_err['Fractional uncertainty per D associated with fit \
    #         parameter'][fit_para]= fsr
        

    _list = []

    for name in ['fractional uncertainty', 'correction factor']:
        for item in simulation_parts:
            _list.append(sys_err['Detector simulation'][item][name])

    for fit_para in fit_paras:
        li = sys_err['Fit parameter uncertainty'][fit_para]
        
        a = reduce(lambda x, y: math.sqrt(x**2+y**2), li)
        _list.append(a)
        
    _list.append(sys_err['Fractional uncertainty per yield'])
    _list.append(sys_err['Fractional uncertainty per D'])

    for fit_para in fit_paras:
        li = sys_err['Fractional uncertainty per D associated with \
fit parameter'][fit_para]
        #_list.append(li)
        a = reduce(lambda x, y: math.sqrt(x**2+y**2), li)
        _list.append(a)

    _list.append(sys_err['Fractional uncertainty per single tag'])

    for fit_para in fit_paras:
        li = sys_err['Fractional uncertainty per single tag associated \
with fit parameter'][fit_para]
        a = reduce(lambda x, y: math.sqrt(x**2+y**2), li)
        _list.append(a)

    _list.append(sys_err['Fractional uncertainty per double tag'])

    return _list

def bf_stat_sys(fit , prefix):
    outfilename = 'bf_stat_sys'
    outfile  = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                              comname=outfilename)
    fdir = outfile.replace(outfilename, '')
    com1_name = 'newfit-cat_files_data.sh'
    com1 = tools.set_file(extbase=attr.brfpath, prefix=prefix, comname=com1_name)
    sdir = com1.replace(com1_name, '')
    com2  = create_bash_stat_syst(fdir, sdir, com1)

    if fit or not os.access(outfile, os.F_OK) :
        print 'Running fitter for stat and syst ...'
        run_bf_fitter(com2, outfile)

def create_bash_stat_syst(fdir, sdir, outfile):
    EXE = attr.fitter
    sys.stdout.write('Using fitter: %s \n' %EXE)
    bash_content = '''#!/usr/bin/env bash
EXE=%s
FDIR=%s
SDIR=%s

YLDFILE=$FDIR/data_yields_for_werner

BKGBRS=$FDIR/data_external_bkg_bfs_for_werner
BKGEFFS=$FDIR/data_bkg_effs_for_werner
BKGERRS=$FDIR/data_bkg_effs_errs_for_werner

SIGSINGEFFS=$FDIR/signal_single_efficiencies_for_werner
SIGSINGERRS=$FDIR/signal_single_efficiencies_errors_for_werner
SIGDOUBEFFS=$FDIR/signal_double_efficiencies_for_werner
SIGDOUBERRS=$FDIR/signal_double_efficiencies_errors_for_werner
SYSTERRORS=$FDIR/newfit-data_systerrors
SEEDS=$FDIR/data_seeds
STATTOSUBTRACT=$FDIR/data_fit_staterrors

echo "#!/usr/bin/env bash" > $SDIR/newfit-data.sh
echo "$EXE <<EOF" >> $SDIR/newfit-data.sh
echo -e "n\\nn" >> $SDIR/newfit-data.sh
cat $FDIR/newfit-modedef >> $SDIR/newfit-data.sh
cat $YLDFILE >> $SDIR/newfit-data.sh
cat $BKGBRS >> $SDIR/newfit-data.sh
cat $SIGSINGEFFS >> $SDIR/newfit-data.sh
cat $SIGDOUBEFFS >> $SDIR/newfit-data.sh
cat $BKGEFFS >> $SDIR/newfit-data.sh
cat $SIGSINGERRS >> $SDIR/newfit-data.sh
cat $SIGDOUBERRS >> $SDIR/newfit-data.sh
cat $BKGERRS >> $SDIR/newfit-data.sh
#echo -e "0\\n0\\n0\\n0\\n0\\n0\\n1\\n1\\n1\\n1\\n1\\n1" >> \
$SDIR/newfit-data.sh
cat $SYSTERRORS >> $SDIR/newfit-data.sh
cat $SEEDS >> $SDIR/newfit-data.sh
echo -e "n\\nn\\ny" >> $SDIR/newfit-data.sh
cat $STATTOSUBTRACT >> $SDIR/newfit-data.sh
echo -e "y" >> $SDIR/newfit-data.sh
cat $FDIR/data_brratiodef >> $SDIR/newfit-data.sh
echo -e "\\ny" >> $SDIR/newfit-data.sh
cat $FDIR/data_crosssectionsdef >> $SDIR/newfit-data.sh
echo "EOF" >> $SDIR/newfit-data.sh
chmod +x $SDIR/newfit-data.sh
''' % (EXE, fdir, sdir)

    fo, bakfile = tools.backup_output(outfile)
    fo.write(bash_content)
    tools.check_output(fo, outfile, bakfile)
    bashfile = outfile
    os.chmod(bashfile, 0755)
    output = commands.getoutput(bashfile)
    if output:
        print 'Stop message from DHadBF:: create_bash_stat_syst:'
        print '-------------------------------------------------'
        print output
        print '-------------------------------------------------'
        sys.exit()
        
    new_bashfile = os.path.join(sdir, 'newfit-data.sh')
    return new_bashfile

   
def get_signal_shape_sys(label):
    if label == '281ipbv12.0':
        tabfile = os.path.join(attr.tabpath, '281ipbv0',
                               'signal_line_shape_syst.txt')
        print 'Loading %s ...' % tabfile
        tab = DHadTable(tabfile)
        line_shape_sys = tab.column_get('Total(%)')
    else:
        tab = get_mode_dependent_syst_tab(label)
        line_shape_sys = tab.row_get('Signal shape')

    return line_shape_sys


def get_fsr_sys(label):
    if label == '281ipbv12.0':
        tabfile = os.path.join(attr.tabpath, '281ipbv0', 'FSR_syst.txt')
        tab = DHadTable(tabfile)
        print 'Loading %s ...' % tabfile
        fsr_sys = tab.column_get('diff X 30%')
    else:
        tab = get_mode_dependent_syst_tab(label)
        fsr_sys = tab.row_get('FSR')
    return fsr_sys 


def get_mode_dependent_syst_tab(label):
    if label in ['818ipbv10', '818ipbv11', '818ipbv12.0']:
        tabdir = '818ipbv7'
    elif label in ['818ipbv12.1']:
        tabdir = '818ipbv12'
    else:
        raise NameError(label)

    tabfile = os.path.join(attr.cbxtabpath, tabdir,
                           'mode_dependent_syst.txt')
    sys.stdout.write('Loading %s ...\n' % tabfile)
    tab = DHadTable(tabfile)
    return tab


        
