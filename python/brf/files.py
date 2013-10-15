"""
Module for Branching Fractions Fitting 

"""

import os
import sys
import attr
import tools 
import shutil
import filecmp

from tools.filetools import BKGFile, UserFile, BrfFile



__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def get_other_files(prefix):

    file_list = ['newfit-modedef',
                 'zero_single_efficiencies_errors_for_werner',
                 'zero_double_efficiencies_errors_for_werner',
                 'data_seeds',
                 'data_brratiodef', 
                 'data_statonly_brratiodef'] 

    for _file in file_list:
        source_file = os.path.join(attr.srcbrfpath, _file)
        if '/generic' in prefix and _file == 'data_seeds':
            source_file += '_generic'
            if '281ipbv0' in prefix:
                source_file += '_281ipbv0'

        dest_file   = tools.set_file(
            extbase   = attr.brfpath, prefix  = prefix, 
            comname   =  _file)

        if os.access(dest_file, os.F_OK) :
            if filecmp.cmp(source_file, dest_file):
                print 'up-to-date: %s' % _file
                continue
            else:
                print 'Updating %s ...' %_file
                shutil.copy2(dest_file, dest_file+'.bak') 
                
        else:
            print 'Copying %s ...' %_file
        shutil.copy2(source_file, dest_file) 


def get_other_files_generic(prefix):
    file_list = ['generic_seeds',
                 'newfit-modedef',
                 'generic_statonly_brratiodef',
                 'generic_statonly_crosssectionsdef'] 

    for _file in file_list:
        source_file = os.path.join(attr.srcbrfpath, _file)
        if '281ipbv0' in prefix:
            if _file == 'generic_seeds':
                source_file += '_281ipbv0'
        elif '281ipbv12' in prefix:
            if _file == 'generic_seeds':
                source_file += '_281ipbv12'
            if 'crosssectionsdef' in _file: 
                source_file += '_281ipb'
        elif '818ipbv12' in prefix:
            if _file == 'generic_seeds':
                source_file += '_818ipbv12'
        else:
            raise NameError(prefix)
        
        dest_file   = tools.set_file(
            extbase   = attr.brfpath, prefix  = prefix, 
            comname   =  _file)

        tools.check_and_copy(source_file, dest_file, verbose=1) 

            
def get_background_files(prefix):
    label = prefix.replace('dir_', '')
    bkg = attr.import_bkg(label)
    
    single_tag_order = bkg.single_tag_order
    fake_mode_order = bkg.fake_mode_order
    fake_mode_list = bkg.fake_mode_list 
    bkg_efficiencies_single = bkg.bkg_efficiencies_single
    dcsd_efficiencies_single = bkg.dcsd_efficiencies_single
    dcsd_pdg_bf = bkg.dcsd_pdg_bf
    scsd_pdg_bf = bkg.scsd_pdg_bf
    scsd_efficiencies_single = bkg.scsd_efficiencies_single
    efficiencies_single = bkg.efficiencies_single
    pdg_bf = bkg.pdg_bf

    bkgeffsname = 'data_bkg_effs_for_werner'
    bkgeffserrsname = 'data_bkg_effs_errs_for_werner'
    if '/generic' in label:
        bkgeffsname = bkgeffsname.replace('data_', 'generic_')
        bkgeffserrsname = bkgeffserrsname.replace('data_', 'generic_')


    bkgeffs = tools.set_file(extbase=attr.brfpath,
                             prefix=prefix, comname=bkgeffsname)
    bkgeffserrs = tools.set_file(extbase=attr.brfpath,
                                 prefix=prefix, comname=bkgeffserrsname)

    f2 = open(bkgeffs+'.tmp', 'w+')
    f3 = open(bkgeffserrs+'.tmp', 'w+')

    # file format is by columns within rows.  The matrix is [effmatrix][BFs],
    # [BFs] as a column matrix.  Hence effectively we print the fake rate for 
    # all the fake types within each signal channel
    for i in single_tag_order:
        # repeat since separate yields for charge conjugate modes of fakes
        # two lines each except for pion-riffic modes, for which we have 
        # only one fake rate
        for j in fake_mode_order:
            if j not in fake_mode_list:
                f2.write('0\n0\n')
                f3.write('0\n0\n')
            elif i == fake_mode_list[j]:
                if j in ('3pi', '3pipi0', '5pi'):
                    f2.write('%f\n' % bkg_efficiencies_single[j])
                    f3.write('0\n')
                elif j in ('kpi', 'kpipi0', 'k3pi', 'kkspibar'):
                    f2.write('0\n%f\n' % bkg_efficiencies_single[j])
                    f3.write('0\n0\n')
                else:
                    f2.write('%f\n0\n' % bkg_efficiencies_single[j])
                    f3.write('0\n0\n')
            else:
                if j in ('3pi', '3pipi0', '5pi'):
                    f2.write('0\n')
                    f3.write('0\n')
                else:
                    f2.write('0\n0\n')
                    f3.write('0\n0\n')
 
        # now, do charge conjugate mode of signal mode
        for j in fake_mode_order:
            if j not in fake_mode_list:
                f2.write('0\n0\n')
                f3.write('0\n0\n')
            elif i == fake_mode_list[j]:
                if j in ('3pi', '3pipi0', '5pi'):
                    f2.write('%f\n' % bkg_efficiencies_single[j])
                    f3.write('0\n')
                elif j == 'kpi' or j == 'kpipi0' or j == 'k3pi' or j == 'kkspibar':
                    f2.write('%f\n0\n' % bkg_efficiencies_single[j])
                    f3.write('0\n0\n')
                else:
                    f2.write('0\n%f\n' % bkg_efficiencies_single[j])
                    f3.write('0\n0\n')
            else:
                if j in ('3pi', '3pipi0', '5pi'):
                    f2.write('0\n')
                    f3.write('0\n')
                else:
                    f2.write('0\n0\n')
                    f3.write('0\n0\n')


    # Now, we wish to do double tags.  Same deal.
    for (i,j) in attr.PossibleDoubleTags:
        for k in fake_mode_order:
            if k in ('3pi', '3pipi0', '5pi'):
                if `i` == fake_mode_list[k] and `j` == fake_mode_list[k]:
                    e = (2 * bkg_efficiencies_single[k]
                         * efficiencies_single[`j`]*pdg_bf[`j`])
                    f2.write('%f\n' % e)               
                    f3.write('0\n')
                elif `i` == fake_mode_list[k]:
                    e = bkg_efficiencies_single[k]* \
                        efficiencies_single[`j`]*pdg_bf[`j`]
                    f2.write('%f\n' % e)
                    f3.write('0\n')
                elif `j` == fake_mode_list[k]:
                    e= bkg_efficiencies_single[k]* \
                       efficiencies_single[`i`] * pdg_bf[`i`]
                    f2.write('%f\n' % e)
                    f3.write('0\n')
                else:
                    f2.write('0\n')            
                    f3.write('0\n')

            elif k in ('kpi', 'kpipi0', 'k3pi', 'kkspibar'):
                # does D0B->k fake D0->i?
                # then we will only have a double tag if D0 fakes a D0B!
                if `i` == fake_mode_list[k] and `j` == fake_mode_list[k]:
                    e = .5*bkg_efficiencies_single[k]* \
                        dcsd_efficiencies_single[`j`]*dcsd_pdg_bf[`j`]
                    if `j` in scsd_pdg_bf:
                        e += .5*bkg_efficiencies_single[k]* \
                             scsd_efficiencies_single[`j`]*scsd_pdg_bf[`j`]
                    print k, 'fakes', (i,j), 'and C conjugate with eff', e
                    f2.write('%f\n%f\n' % (e,e))
                    f3.write('0\n0\n')
                elif `i` == fake_mode_list[k]:
                    e = .5*bkg_efficiencies_single[k]* \
                        dcsd_efficiencies_single[`j`]*dcsd_pdg_bf[`j`]
                    if `j` in scsd_pdg_bf:
                        e += .5*bkg_efficiencies_single[k]* \
                             scsd_efficiencies_single[`j`]*scsd_pdg_bf[`j`]
                    f2.write('0\n%f\n' % e)
                    f3.write('0\n0\n')
                elif `j` == fake_mode_list[k]:
                    e = .5*bkg_efficiencies_single[k]* \
                        dcsd_efficiencies_single[`i`]*dcsd_pdg_bf[`i`]
                    if `i` in scsd_pdg_bf:
                        e += .5*bkg_efficiencies_single[k]* \
                             scsd_efficiencies_single[`i`]*scsd_pdg_bf[`i`]
                    f2.write('%f\n0\n' % e)
                    f3.write('0\n0\n')
                else:
                    f2.write('0\n0\n')
                    f3.write('0\n0\n')
 

            elif not k in ('kkspibar', 'k3pi', 'd0generic', 'dpgeneric'):
                if `i` == fake_mode_list[k] and `j` == fake_mode_list[k]:
                    e = bkg_efficiencies_single[k]* \
                        efficiencies_single[`j`]*pdg_bf[`j`]
                    f2.write('%f\n%f\n' % (e,e))               
                    f3.write('0\n0\n')
                elif `i` == fake_mode_list[k]:
                    e = bkg_efficiencies_single[k]* \
                        efficiencies_single[`j`]*pdg_bf[`j`]
                    f2.write('%f\n0\n' % e)
                    f3.write('0\n0\n')
                elif `j` == fake_mode_list[k]:
                    e= bkg_efficiencies_single[k]* \
                       efficiencies_single[`i`] * pdg_bf[`i`]
                    f2.write('0\n%f\n' % e)
                    f3.write('0\n0\n')
                else:
                    f2.write('0\n0\n')
                    f3.write('0\n0\n')

            elif k == 'kkspibar':
                if `i` == fake_mode_list[k] and `j` == fake_mode_list[k]:
                    e=efficiencies_single[`i`]* \
                       efficiencies_single[`j`]*pdg_bf[`j`]
                    f2.write('%f\n%f\n' % (e,e))
                    f3.write('0\n0\n')
                elif `i` == fake_mode_list[k]:
                    e=efficiencies_single[`i`]* \
                       efficiencies_single[`j`]*pdg_bf[`j`]
                    f2.write('0\n%f\n' % e)
                    f3.write('0\n0\n')
                elif `j` == fake_mode_list[k]:
                    e=efficiencies_single[`j`]* \
                       efficiencies_single[`i`]*pdg_bf[`i`]
                    f2.write('%f\n0\n' % e)
                    f3.write('0\n0\n')
                else:
                    f2.write('0\n0\n')
                    f3.write('0\n0\n')
                    
            else:
                f2.write('0\n0\n')
                f3.write('0\n0\n')

    f2.close()
    f3.close()
    
    for bkg_file in  [ bkgeffs, bkgeffserrs]:
        source_file = bkg_file + '.tmp'
        dest_file = bkg_file

        if os.access(dest_file, os.F_OK) :
            if filecmp.cmp(source_file, dest_file):
                sys.stdout.write('up-to-date: %s\n' % bkg_file)
                continue
            else:
                sys.stdout.write('Updating %s ...' %bkg_file)
                shutil.copy2(dest_file, dest_file+'.bak') 
                sys.stdout.write(' OK.\n')
        else:
            sys.stdout.write('Creating %s ...' %bkg_file)
        shutil.copy2(source_file, dest_file) 
        sys.stdout.write(' OK.\n')


def get_external_bkg_files(prefix):
    label = prefix.replace('dir_', '')
    bkg_file_list = ['data_external_bkg_bfs_for_werner',
                     'data_statonly_external_bkg_bfs_for_werner']

    for bkg_file in bkg_file_list:
        source_file = os.path.join(attr.srcbrfpath, bkg_file)
        if label in ['818ipbv10', '818ipbv7/generic', '818ipbv12.1',
                     '818ipbv12.2']:
            
            source_file += '_'+label
            if label == '818ipbv7/generic':
                source_file = source_file.replace('/generic', '_generic')
            if label == '818ipbv12.2':
                source_file = source_file.replace('v12.2', 'v12.1')

        dest_file   = tools.set_file(
            extbase   = attr.brfpath, prefix  = prefix, 
            comname   =  bkg_file)

        if '281ipb' in label or label in ['818ipbv12.0', '818ipbv12.0/generic',
                                          '818ipbv12.1', '818ipbv12.2',
                                          '818ipbv12.3', '818ipbv12.4']:
            shutil.copy2(source_file, dest_file) 
        elif '537ipb' in label:
            factor = 1.91
            scale_absolute_bkgs(source_file, dest_file, factor)
        elif label in ['818ipbv7', '818ipbv8', '818ipbv9']:
            factor = 2.91
            scale_absolute_bkgs(source_file, dest_file, factor)
        else:
            raise NameError(prefix)


def get_external_bkg_files_generic(prefix):
    label = prefix.replace('dir_', '').replace('/generic', '')
    bkg_file_list = ['generic_external_bkg_bfs_for_werner']

    for bkg_file in bkg_file_list:
        source_file = os.path.join(attr.srcbrfpath, bkg_file)
        if '281ipbv0' in label:
            source_file += '_281ipbv0'
        elif '281ipbv12' in label:
            source_file += '_281ipbv12'
            if '281ipbv12.2' in label:
                source_file += '.2'
        elif '818ipbv12' in label:
            source_file += '_818ipbv12'
            if '818ipbv12.2' in label:
                source_file += '.2'
        else:
            raise NameError(label)

        dest_file   = tools.set_file(
            extbase   = attr.brfpath, prefix  = prefix, 
            comname   =  bkg_file)

        tools.check_and_copy(source_file, dest_file, verbose=1) 


def scale_absolute_bkgs(infile, outfile, factor):

    b = BKGFile(infile)
    b.scale(factor)
    b.output(outfile, verbose=1)


def get_data_statonly_crosssectionsdef(prefix):
    filename = 'data_statonly_crosssectionsdef'
    file_ = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                           comname=filename)
    if '281ipb' in prefix:
        lumi = '281.50'
    elif '537ipb' in prefix:
        lumi = '536.57'
    elif '818ipb' in prefix:
        lumi = '818.10'
    else:
        raise NameError(prefix)

    content = '''0
4
%s
0.
0
n
0
n
n
n
''' % lumi

    f = UserFile()
    f.append(content)
    f.output(file_, verbose=1)

def get_data_crosssectionsdef(prefix):
    filename = 'data_crosssectionsdef'
    file_ = tools.set_file(extbase=attr.brfpath, prefix=prefix, 
                           comname=filename)
    if '281ipb' in prefix:
        lumi = '281.50'
        lumi_err = '2.8150'
    elif '537ipb' in prefix:
        lumi = '536.57'
        lumi_err = '5.3657'
    elif '818ipb' in prefix:
        lumi = '818.10'
        lumi_err = '8.1810'
    else:
        raise NameError(prefix)

    bffilename = 'bf_stat'
    bffile = tools.set_file(extbase=attr.brfpath, prefix=prefix,
                            comname=bffilename)
    brf = BrfFile(bffile)

    ne_xsec_err = brf.parsed['sigma(D0D0bar)'].split('+-')[-1].strip()
    ch_xsec_err = brf.parsed['sigma(D+D-)'].split('+-')[-1].strip()
    xsec_err =  brf.parsed['sigma(DDbar)'].split('+-')[-1].strip()
    xsec_ratio_err = brf.parsed['chg/neu'].split('+-')[-1].strip()

    content = '''0
4
%s
%s
0
y
%s
0
y
%s
y
%s
y
%s
''' % (lumi, lumi_err, ne_xsec_err, ch_xsec_err, xsec_err, xsec_ratio_err)

    f = UserFile()
    f.append(content)
    f.output(file_, verbose=1)


