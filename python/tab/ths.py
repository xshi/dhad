"""
Script for Thesis related tables

"""

import os
import sys
import attr
import ths
import tools
import cbx

from tools import THSTable, parse_result
from attr.modes import modes
from attr import cbxtabpath, fitbase, get_dcsd_correction, \
     get_pi0_eff_correction
from tools.filetools import BrfFile, PDLFile
from brf import yields_and_efficiencies


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    tabname = args[0]
    label = args[1]
    function = getattr(ths, tabname)
    return function(opts, tabname, label)


def dt_dz_eff_yield(opts, tabname, label):
    tab = THSTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double-dz')

    tabfile = os.path.join(cbxtabpath, '818ipbv12', 'doubletageff.txt')
    tab.column_append_from_tab_file('Efficiency(%)', tabfile,
                                    'Efficiency(%)', row=':10')
    tabfile = os.path.join(cbxtabpath, label, 'datadoubletagyields.txt')
    tab.column_append_from_tab_file('Data Yield', tabfile,
                                    '25.2 MeV', row=':10')
    tab.column_append_from_tab_file('Background', tabfile,
                                    'Bkgd', row='10:')

    texhead = r'''Double tag mode  & Efficiency(\%) & Data yield  & Background '''
    tab.output(tabname, texhead)


def dt_dp_eff_yield(opts, tabname, label):
    tab = THSTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double-dp')

    tabfile = os.path.join(cbxtabpath, '818ipbv12', 'doubletageff.txt')
    tab.column_append_from_tab_file('Efficiency(%)', tabfile,
                                    'Efficiency(%)', row='10:')

    tabfile = os.path.join(cbxtabpath, label, 'datadoubletagyields.txt')
    tab.column_append_from_tab_file('Data Yield', tabfile,
                                    '25.2 MeV', row='10:')
    tab.column_append_from_tab_file('Background', tabfile,
                                    'Bkgd', row='10:')

    texhead = r'''Double tag mode  & Efficiency(\%) & Data yield  & Background '''
    tab.output(tabname, texhead)

def st_eff_yield(opts, tabname, label):
    tab = THSTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tabfile = os.path.join(cbxtabpath, '818ipbv12',
                           'singletag_sigmc_eff.txt')
    tab.column_append_from_tab_file('Efficiency(%)', tabfile,
                                    'Efficiency(%)')
    tabfile = os.path.join(cbxtabpath, label, 'singletag_data_yield.txt')
    tab.column_append_from_tab_file('Data Yield', tabfile,
                                    'Gamma 25.2 MeV')
    tab.column_append_from_tab_file('Background', tabfile, 'Bkgd')

    texhead = r'''Single tag mode  & Efficiency(\%) & Data yield  & Background '''
    tab.output(tabname, texhead)


def singletag_data_yield_widede(opts, tabname):
    tab = THSTable()
    tabprefix = 'dir_818ipbv12'
    tab.column_append_from_dict('Mode', 'fname,fnamebar')     
    tab.column_append_from_files('Yield1(regular)', 'N1,N2',  fitbase,
                                 tabprefix, 'd', 's', 'txt', rnd='1.')
    tab.column_append_from_files('Yield2(widede)', 'N1,N2',  fitbase,
                                 tabprefix+'/widede', 'd', 's', 'txt', rnd='1.')
    tab.column_append_by_divide('Yield1/Yield2',  'Yield1(regular)',
                                'Yield2(widede)', 'Efcy', '.0001') 
    tab.column_append_from_files('eff1(regular)', 'N1,N2', fitbase,
                                 tabprefix, 's', 's', 'txt', rnd='1.')
    tab.column_append_from_files('eff2(widede)', 'N1,N2', fitbase,
                                 tabprefix+'/widede', 's', 's', 'txt', rnd='1.')
    tab.column_append_by_divide('eff1/eff2', 'eff1(regular)', 'eff2(widede)', 
                                'Efcy', '.0001') 
    tab.column_append_by_divide('Ratio', 'Yield1/Yield2', 'eff1/eff2', 
                                'Indp', '.001') 

    tab.columns_delete(['Yield1(regular)', 'Yield2(widede)',
                        'eff1(regular)', 'eff2(widede)'])
    
    texhead = r'''Mode	 & Yield1/Yield2  & eff1/eff2 & Ratio'''
    tab.output(tabname, texhead)


def vary_argus_single(opts, tabname):
    tab = THSTable()
    tabprefix = 'dir_818ipbv12'
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    titles = ['argus_low', 'std', 'argus_high']
    tab.column_append_from_files(titles[0], 'N1,N2', fitbase,
                                 tabprefix+'/argus_low', 'd', 's', 'txt')
    tab.column_append_from_files(titles[1], 'N1,N2', fitbase, tabprefix,  
                                 'd', 's', 'txt')
    tab.column_append_from_files(titles[2], 'N1,N2', fitbase,
                                 tabprefix+'/argus_high', 'd', 's', 'txt')

    std = titles[1]
    colA = titles[0]
    colB = titles[2]
    headA = 'diff(%s)' %colA
    headB = 'diff(%s)' %colB
    headC = 'max-diff(%)'
    tab.column_append_by_diff_pct(headA, colA, std)
    tab.column_append_by_diff_pct(headB, colB, std)
    tab.column_append_by_max(headC, headA, headB)
    tab.columns_delete([headA, headB])
    tab.columns_trim(titles, rnd='1.')

#    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
#    & ARGUS Low & Std  & ARGUS High & (\%)  '''
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
    & ARGUS Low & Std  & ARGUS High & (\%)  '''
    tab.output(tabname, texhead)


def mode_dependent_syst(opts, tabname):
    tab = THSTable()
    tabprefix = 'dir_818ipbv12'
    modenames = [modes[mode]['sname'] for mode in modes]
    modenames.insert(0, 'Source')
    tab.row_append(modenames)
    tab.row_append(cbx.mode_syst_signal_shape(tabprefix))
    tab.row_append(cbx.mode_syst_tracking(tabprefix))
    tab.row_append(cbx.mode_syst_ks(tabprefix), 'Eff($\KS$)')
    tab.row_append(cbx.mode_syst_pi0(tabprefix), 'Eff($\pi^0$)')
    tab.row_append(cbx.mode_syst_pid_pion(tabprefix), 'PID - $\pipm$')
    tab.row_append(cbx.mode_syst_pid_kaon(tabprefix), 'PID - $\Kpm$ ')
    tab.row_append(cbx.mode_syst_lepton_veto(tabprefix))
    tab.row_append(cbx.mode_syst_de(tabprefix), '$|\DeltaE|$ (*)')
    tab.row_append(cbx.mode_syst_bkg_shape(tabprefix), 'Bkgd shape')
    tab.row_append(cbx.mode_syst_fsr(tabprefix))
    tab.row_append(cbx.mode_syst_substructure(tabprefix))
    tab.row_append(cbx.mode_syst_multcand(tabprefix))

    texhead = r'''Source & $K\pi$ & $K\pi\pi^0$ & $K\pi\pi\pi$ & $K\pi\pi$ & $K\pi\pi\pi^0$ & $K_S^0\pi$ & $K_S^0\pi\pi^0$ & $K_S^0\pi\pi\pi$ & $KK\pi$ '''
    tab.output(tabname, texhead)

    
def fitResultsMC(opts, tabname, label):
    bffilename = 'bf_stat'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)

    if '281ipbv0' in label and '/generic' in label:
        generated = attr.Generic281v0_NBF
        power = '10E6'
        factor = 0.000001
    else:
        raise NameError(label)

    tab = THSTable()
    tab.column_append(parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(generated, 'Input value')
    tab.column_append(parse_result(bffile, 'value_err'), 'Fitted value')

    tab.column_append_by_diff_sigma('Difference', 'Fitted value',
                                    'Input value')
    tab.column_trim('Fitted value', row=['ND0D0Bar', 'ND+D-'],
                    rnd='.001', factor=factor, opt='(cell)x%s' %power)
    tab.column_trim('Fitted value', rnd='.00001',
                    except_row=['ND0D0Bar', 'ND+D-'])
    tab.column_append(parse_result(bffile, 'err_frac'),
                      'Frac. Err', rnd='.1', opt='~(cell%)')
    
    tab.columns_join('Fitted value','Fitted value','Frac. Err', str=' ')

    tab.column_trim('Input value', row=['ND0D0Bar', 'ND+D-'],
                    rnd='.001', factor=factor, opt='cellx%s'%power)
    tab.output(tabname, trans_dict=attr.NBF_dict)

    diff_from_seeds = 'chisq 13.5813 ndof 11 prob 0.257036'
    sys.stdout.write('%s\n' %diff_from_seeds)
    sys.exit()
    chisq = tab.cell_get_by_square_sum(column='Difference')
    ndof = 11
    from ROOT import TMath
    prob = TMath.Prob(float(chisq), ndof)
    prob = tab.cell_trim(prob, rnd='.1', factor=100)
    sys.stdout.write('Chisq is %s for %s d.o.f, Prob = %s%% \n' % (
        chisq, ndof, prob))
    

def fitResultsData(opts, tabname, label):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)
    tab = THSTable()
    tab.column_append(parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(parse_result(bffile, 'value'), 'value')
    tab.column_append(parse_result(bffile, 'stat'),  'stat')
    tab.column_append(parse_result(bffile, 'syst'),  'syst')
    tab.column_append_by_divide('Stat.(%)', 'stat', 'value',
                                rnd='.1', factor=100)
    tab.column_append_by_divide('Syst.(%)', 'syst', 'value',
                                rnd='.1', factor=100)
    tab.columns_join3('Fitted value', 'value', 'stat',  'syst')
    tab.column_trim('Fitted value', row=['ND0D0Bar', 'ND+D-'],
                    rnd='.001', factor=0.000001, opt='(cell)x10E6')
    tab.column_trim('Fitted value', rnd='.001', factor=100,
                    except_row = ['ND0D0Bar', 'ND+D-'], opt='(cell)%')
    texhead = r'''Parameter & Fitted value & \multicolumn{2}{c}{Fractional error}\\[-0.6ex] & & Stat.(\%) & Syst.(\%)'''
    tab.output(tabname, texhead, trans_dict=attr.NBF_dict)


def fitResultsRatiosData(opts, tabname, label):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)
    tab = THSTable()
    tab.column_append(parse_result(bffile, 'para_bf_ratio'),
                      'Parameters')
    tab.column_append(parse_result(bffile, 'value_bf_ratio'), 'value')
    tab.column_append(parse_result(bffile, 'stat_bf_ratio'), 'stat')
    tab.column_append(parse_result(bffile, 'syst_bf_ratio'), 'syst')
    tab.column_append_by_divide('Stat.(%)', 'stat', 'value',
                                rnd='.1', factor=100)
    tab.column_append_by_divide('Syst.(%)', 'syst', 'value',
                                rnd='.1', factor=100)
    tab.columns_join3('Fitted value','value','stat','syst', rnd='.001')
    texhead = r'''Parameter & Fitted value & \multicolumn{2}{c}{Fractional error}\\[-0.6ex] & & Stat.(\%) & Syst.(\%)'''
    tab.output(tabname, texhead, trans_dict=attr.BF_Ratio_dict)

    
def yieldDTResidualsDataDz(opts, tabname, label):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)
    tab = THSTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double-dz')
    tab.column_append(parse_result(bffile, 'residual_double_dz'),
                      'Residual', rnd = '1.')
    tab.output(tabname, trans_dict=attr.BF_Ratio_dict)


def yieldDTResidualsDataDp(opts, tabname, label):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)
    tab = THSTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double-dp')
    tab.column_append(parse_result(bffile, 'residual_double_dp'),
                      'Residual', rnd = '1.')
    tab.output(tabname, trans_dict=attr.BF_Ratio_dict)

def crossSections(opts, tabname, label):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix='dir_'+label, comname=bffilename)

    brf = BrfFile(bffile)
    tab = THSTable()
    tab.row_append(['Quantity', 'Value'])
    names = ['sigma(D0D0bar)', 'sigma(D+D-)',
             'sigma(DDbar)', 'chg/neu']
    for name in names:
        row = [name, brf.parsed[name]]
        if name == 'chg/neu':
            tab.row_append(row, rnd='.001')   
        else:
            name = row[0]
            value = row[1]
            value = tab.cell_trim(
                cell=value, factor=0.001, rnd='.001',
                opt='(cell){~\\rm nb}')
            row = [name, value]
            tab.row_append(row)

    tab.output(tabname, trans_dict=attr.cross_sections_dict)
    sys.stdout.write('%s\n' % brf.parsed['coeff_ddbar'])
