"""
Script for CBX related tables

"""

import os
import sys
import attr
import cbx
import tools

from tools import DHadCBXTable, data_bkg_double, matrix_inv_cov_epsilon,\
     data_bkg_single, parse_result, get_multspec_reweight, \
     get_corrected_abs_bkg, get_eff_matrix_sideband, get_yld_vector_sideband,\
     get_generic_mctruth, parse_opts_set, str_to_ufloat, calc_asy_syst
from attr.modes import modes
from attr import get_generated_numbers, fitbase, evtlogbase, cbxtabpath,\
    get_dcsd_correction, get_pi0_eff_correction, get_cp_asymmetry
from tools.filetools import BrfFile, PDLFile
from brf import yields_and_efficiencies
from math import sqrt 

__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010-2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    tabname = args[0]
    label = args[1]
    tabprefix = 'dir_%s' %label
    function = getattr(cbx, tabname)
    return function(opts, tabname, tabprefix)


def brf_chisq(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    if '/generic' in tabprefix:
        bffilename = 'bf_stat'

    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    brf = BrfFile(bffile)
    sys.stdout.write('%s\n' % brf.parsed['chisq'])


def brf_results(opts, tabname, tabprefix):
    tabnames = ['crossSections', 'fitResultsData', 'fitResultsRatiosData',
                'correlationMatrixData', 'yieldSTResidualsData',
                'yieldDTResidualsData', 'singletag_data_yield',
                'datadoubletagyields', 'fitResultsDataVariations'
                ]
    for tn in tabnames:
        fn = getattr(cbx, tn)
        fn(opts, tn, tabprefix)


def compare_yields_DDbar(opts, tabname, tabprefix):
    dt_type_list = ['d', 's']
    tag = 's'
    variable = 'yields'
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname')

    for dt_type in dt_type_list:
        type_name = attr.TypeNames[dt_type]
        col_name  = '%s diff(%%)' %type_name
        tmp_tab = DHadCBXTable()
        tmp_tab.column_append_from_dict('Mode', 'fname,fnamebar')     
        tmp_tab.column_append_from_files(
            '%s yield (%s)' %(type_name, tabname),  'N1,N2', fitbase,
            tabprefix, dt_type, tag ,'txt', rnd='1.')
        tmp_tab.rows_join_by_diff_pct(
            col_name,err_type='Indp',denominator='first')
        tab.column_append(tmp_tab.column_get(col_name))

    tab.output(tabname, tabprefix=tabprefix)


def compare_yields_data_double(opts, tabname, tabprefix):
    tag = 'd'
    ndof = 45 
    variable = 'yields'
    dt_type = 'data'
    tab_A = tabprefix.split(',')[0].replace('dir_', '')
    tab_B = tabprefix.split(',')[1]
    
    label_A, fitbase_A, prefix_A = tools.parse_tabname(opts, tab_A) 
    label_B, fitbase_B, prefix_B = tools.parse_tabname(opts, tab_B) 

    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', opt='double')
    tab.column_append_from_files(label_A, 'N', fitbase_A, prefix_A,
                                 dt_type, tag ,'txt', rnd='1.')
    if '281ipb' in tab_A and '537ipb' in tab_B:
        factor = 1.91
        label_A = 'Scaled_%s' % label_A
        tab.column_append_from_files(label_A, 'N', fitbase_A,
                                     prefix_A, dt_type, tag ,'txt', rnd='1.',
                                     factor=factor)

    tab.column_append_from_files(label_B, 'N', fitbase_B, prefix_B,
                                 dt_type, tag ,'txt', rnd='1.')

    tab.column_append_by_diff_chisq('chisq', label_B, label_A, rnd='.1')

    chisq = tab.column_get('chisq')

    total_chisq = sum(chisq[1:])
    from ROOT import TMath
    prob = TMath.Prob(total_chisq, ndof)
    prob = tab.cell_trim(prob, rnd='.1', factor=100)

    tab.row_append(['', '', '', 'Total $\chi^2$', total_chisq])
    tab.row_append(['', '', '', '$p(\chi^2)$', '%s%%' % prob])
    tab.row_hline('Dp_to_KKpi Dm_to_KKpi')

    texhead = r'''Mode & DT(281 $pb^{-1}$) & Scaled DT (281 $pb^{-1}$) & DT(537 $pb^{-1}$) & $\chi^2$ '''
      
    tab.output(tabname, texhead, tabprefix=tabprefix)


def compare_yields_data_single(opts, tabname, tabprefix):
    tag = 's'
    ndof = 18 
    variable = 'yields'
    dt_type = 'data'
    label_A = tabprefix.split(',')[0].replace('dir_', '')
    label_B = tabprefix.split(',')[1]

    fitbase = attr.fitbase 
    
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tab.column_append_from_files(label_A, 'N1,N2', fitbase, 'dir_%s' %label_A,
                                 dt_type, tag ,'txt', rnd='1.')

    if '281ipb' in label_A and '537ipb' in label_B:
        factor = 1.91
        prefix = 'dir_%s' %label_A
        label_A = 'Scaled_%s' % label_A
        tab.column_append_from_files(label_A, 'N1,N2', fitbase,
                                     prefix, dt_type, tag, 'txt',
                                     rnd='1.', factor=factor)

    tab.column_append_from_files(label_B, 'N1,N2', fitbase, 'dir_%s' % label_B,
                                 dt_type, tag ,'txt', rnd='1.')

    tab.column_append_by_diff_chisq('chisq', label_B, label_A, rnd='.1')

    chisq = tab.column_get('chisq')

    total_chisq = sum(chisq[1:])
    from ROOT import TMath
    prob = TMath.Prob(total_chisq, ndof)
    prob = tab.cell_trim(prob, rnd='.1', factor=100)

    tab.row_append(['', '', '', 'Total $\chi^2$', total_chisq])
    tab.row_append(['', '', '', '$p(\chi^2)$', '%s%%' % prob])
    tab.row_hline('Dm_to_KKpi')

    texhead = r'''Mode & ST(281 $pb^{-1}$) & Scaled ST (281 $pb^{-1}$) & ST(537 $pb^{-1}$) & $\chi^2$ '''
      
    tab.output(tabname, texhead, tabprefix=tabprefix)


def correlationMatrixData(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)

    tab = DHadCBXTable()
    tab.input_list(parse_result(bffile, 'corr_coef'), rnd='.01')

    for row in range(11):
        for col in range(11):
            if row > col :
                tab.cell_set(row, col, '.')

    global_corr = parse_result(bffile, 'global_corr')
    tab.row_append(global_corr[1:], rnd='.01')

    tab.row_hline(10)
    tab.output(tabname, tabprefix=tabprefix)

    
def correlationMatrixMC(opts, tabname, tabprefix):
    bffilename = 'bf_stat'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)

    tab = DHadCBXTable()
    tab.input_list(parse_result(bffile, 'corr_coef'), rnd='.01')

    for row in range(11):
        for col in range(11):
            if row > col :
                tab.cell_set(row, col, '.')

    global_corr = parse_result(bffile, 'global_corr')[1:]

    tab.row_append(global_corr, rnd='.01')

    tab.row_hline(10)
    tab.output(tabname, tabprefix=tabprefix)


def CPAsymmetries(opts, tabname, tabprefix):
    label = tabprefix.replace('dir_', '')
    if '281ipb' in label:
        dt_file = os.path.join(attr.base, '7.06/tab/cbx_single_data_gamma.txt')
        eff_file = os.path.join(attr.base, '7.06/tab/cbx_single_signal_eff.txt')
        yldname = 'Gamma 28.6 MeV'
        bkgname = 'Bkgd'
        effname = 'Efficiency(%)'
    elif '818ipb' in label:
        dt_file = os.path.join(attr.cbxtabpath, 
                               '818ipbv12.2/singletag_data_yield.txt')
        eff_file = os.path.join(attr.cbxtabpath, 
                               '818ipbv12/singletag_sigmc_eff.txt')
        yldname = 'Gamma 25.2 MeV'
        bkgname = 'Bkgd'
        effname = 'Efficiency(%)'
    else:
        raise NameError(label)
    
    dt = DHadCBXTable(dt_file)
    eff = DHadCBXTable(eff_file)
    
    tab = DHadCBXTable()
    tab.row_append(['Mode', 'CP Asymmetry (%)'])

    for mode in modes:
        fname = modes[mode]['fname']
        fnamebar = modes[mode]['fnamebar']
        yld = dt.cell_get(fname, yldname)
        yldbar = dt.cell_get(fnamebar, yldname)
        bkg = dt.cell_get(fname, bkgname)
        effs = eff.cell_get(fname, effname)
        effsbar = eff.cell_get(fnamebar, effname)

        bkgerr = parse_opts_set(opts.set, 'bkgerr')
        if bkgerr == 0:
            bkg = bkg.split('+/-')[0]
        
        N = (str_to_ufloat(yld) - str_to_ufloat(bkg))/str_to_ufloat(effs)
        Nbar = (str_to_ufloat(yldbar) - str_to_ufloat(bkg))/str_to_ufloat(effsbar)
        acp = (N - Nbar)/(N + Nbar)

        syst = calc_asy_syst(label, mode)

        acp = tab.cell_trim('%s +/- %s' % (acp, syst), factor=100, rnd='.1')
        tab.row_append([fname, acp])
    
    tab.output(tabname, tabprefix=tabprefix)


def CPAsymmetrySystematics(opts, tabname, tabprefix):
     label = tabprefix.replace('dir_', '')
     tab = DHadCBXTable()
     headers = ['Efficiency', 'Data Asymmetry (%)', 'MC Asymmetry (%)',
                'Data-MC Difference (%)', 'Systematic (%)']
     tab.row_append(headers)
     names = ['K tracking', 'K PID', 'pi tracking', 'pi PID']

     for name in names:
          tab.row_append(get_cp_asymmetry(name, label))

     for head in headers:
          tab.column_trim(head, factor=100, rnd='.01')
          
     tab.column_replace('Efficiency', [
             'Efficiency', 'K tracking', 'K PID', '$\pi$ tracking', '$\pi$ PID'])
     tab.output(tabname, tabprefix=tabprefix, outputtxt=True)

     
def crossfeedeffs(opts, tabname, tabprefix):
    yldfile = tools.set_file(
        extbase = attr.brfpath, prefix = tabprefix, 
        comname = 'yields_and_efficiencies')

    if not os.access(yldfile, os.F_OK): 
        label = tabprefix.replace('dir_', '')
        yldfile = yields_and_efficiencies(opts, [label])

    tab = DHadCBXTable()
    row = ['From', 'To', 'Efficiency']
    tab.row_append(row)

    f = open(yldfile, 'r')
    for line in f:
        idstring = line.split(': ')[0]+':'

        #if 'fakes' in idstring :
        if idstring in attr.used_crossfeeds:
            items = line.split()
            fname = items[0]
            fnameb = items[2].replace(':', '')
            yldsigma = items[3]
            entries = items[4]
            yld = items[5]
            ratio = items[6]
            if float(ratio) < 0.0008:
                continue
            ratioerr = items[7]
            row = [fname, fnameb, '%s +/- %s' %(ratio, ratioerr)]
            tab.row_append(row)
    f.close()
    tab.column_trim('Efficiency', rnd='.1', factor=10000)
    tex_dict = attr.single_tex_dict
    tab.column_replace_by_translation('From', tex_dict)
    tab.column_replace_by_translation('To', tex_dict)
    texhead = r'''From  & To & Efficiency ($\times 10^{-4}$ \%)'''
    tab.output(tabname, texhead, tabprefix=tabprefix)


def crossSections(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)

    brf = BrfFile(bffile)
    tab = DHadCBXTable()
    tab.row_append(['Name', 'Value'])
    names = ['sigma(D0D0bar)', 'sigma(D+D-)', 'sigma(DDbar)', 'chg/neu']
    for name in names:
        row = [name, brf.parsed[name]]
        if name == 'chg/neu':
            tab.row_append(row, rnd='.001')   
        else:
            name = row[0]
            value = row[1]
            value = tab.cell_trim(
                cell=value, factor=0.001, rnd='.001', opt='(cell){~\\rm nb}')
            row = [name, value]
            tab.row_append(row)

    texstyle = 'eqnarray'
    tab.output(tabname, trans_dict=attr.cross_sections_dict,
               texstyle=texstyle, tabprefix=tabprefix)

    sys.stdout.write('%s\n' % brf.parsed['coeff_ddbar'])
    

def datadoubletagyields(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    bkgprefix = tabprefix
    if '.' in tabprefix:
        tabprefix = tabprefix.split('.')[0]
    
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')     
    tab.column_append_from_files(
        '22.7 MeV', 'N', fitbase, tabprefix+'/gamma/0.0227',
        'd', 'd',  'txt', rnd='1.')
    tab.column_append_from_files(
        '25.2 MeV', 'N',  fitbase, tabprefix, 'd', 'd',  'txt', rnd='1.')
    tab.column_append_from_files(
        '27.7 MeV', 'N',  fitbase, tabprefix+'/gamma/0.0277',
        'd', 'd',  'txt', rnd='1.')
    tab.column_append(data_bkg_double(opts, bkgprefix), 'Bkgd')
    tab.column_trim('Bkgd', rnd = '.1', err_type='<0.1')
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield}  & Background \\
        &   $\Gamma=22.7$ MeV  & $\Gamma=25.2$ MeV  & $\Gamma=27.7$ MeV  &  '''
    tab.output(tabname, texhead, tabprefix=bkgprefix, outputtxt=True)


def dcsd_correction(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double-dz')
    tab.column_append(get_dcsd_correction(), 'Yield correction factor',
                      rnd='.001')
    tab.output(tabname, outputtxt=True, tabprefix=tabprefix)
    

def doubletag_data_yield_widede(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')     
    tab.column_append_from_files('Yield1(regular)', 'N',  fitbase,
                                 tabprefix, 'd', 'd', 'txt', rnd='1.')
    tab.column_append_from_files('Yield2(widede)', 'N',  fitbase,
                                 tabprefix+'/widede', 'd', 'd', 'txt',
                                 rnd='1.')
    tab.column_append_by_divide('Yield1/Yield2',  'Yield1(regular)',
                                'Yield2(widede)', 'Efcy', '.0001') 
    tab.column_append_from_files('eff1(regular)', 'N', fitbase,
                                 tabprefix, 's', 'd', 'txt', rnd='1.')
    tab.column_append_from_files('eff2(widede)', 'N', fitbase,
                                 tabprefix+'/widede', 's', 'd', 'txt',
                                 rnd='1.')
    tab.column_append_by_divide('eff1/eff2', 'eff1(regular)', 'eff2(widede)', 
                                'Efcy', '.0001')
    tab.column_append_by_divide('Ratio', 'Yield1/Yield2', 'eff1/eff2', 
                                'Indp', '.001') 
    tab.column_append_from_files('eff1(noFSR)', 'N', fitbase,
                                 tabprefix+'/nofsr', 's', 'd', 'txt',
                                 rnd='1.')
    tab.column_append_from_files('eff2(widede_noFSR)', 'N',  fitbase,
                                 tabprefix+'/widede/nofsr', 's', 'd',
                                 'txt', rnd='1.')
    tab.column_append_by_divide('eff1(noFSR)/eff2(widede_noFSR)',
                                'eff1(noFSR)', 'eff2(widede_noFSR)', 
                                'Efcy', '.001') 
    tab.columns_delete(['Yield1(regular)', 'Yield2(widede)', 'eff1(regular)',
                        'eff2(widede)', 'eff1(noFSR)', 'eff2(widede_noFSR)'])
    texhead = r'''Mode	 & Yield1/Yield2  & eff1/eff2 & Ratio & eff1'/eff2' '''
    tab.output(tabname, texhead, tabprefix=tabprefix)


def doubletag_de_syst(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')     
    tab.column_append_from_files('Yield1(regular)', 'N',  fitbase,
                                 tabprefix, 'd', 'd', 'txt', rnd='1.')
    tab.column_append_from_files('Yield2(widede)', 'N',  fitbase,
                                 tabprefix+'/widede', 'd', 'd', 'txt',
                                 rnd='1.')
    tab.column_append_by_divide('Yield1/Yield2',  'Yield1(regular)',
                                'Yield2(widede)', 'Efcy', '.0001') 
    tab.column_append_from_files('eff1(regular)', 'N', fitbase,
                                 tabprefix, 's', 'd', 'txt', rnd='1.')
    tab.column_append_from_files('eff2(widede)', 'N', fitbase,
                                 tabprefix+'/widede', 's', 'd', 'txt',
                                 rnd='1.')
    tab.column_append_by_divide('eff1/eff2', 'eff1(regular)', 'eff2(widede)', 
                                'Efcy', '.0001')
    tab.column_append_by_divide('Ratio', 'Yield1/Yield2', 'eff1/eff2', 
                                'Indp', '.001') 
    tab.columns_delete(['Yield1(regular)', 'Yield2(widede)', 'eff1(regular)',
                        'eff2(widede)', 'Yield1/Yield2', 'eff1/eff2'])
    tab.column_append_by_subtract_number('Syst (%)', 'Ratio', '1',
                                         rnd='.01', factor=100, err_type='None')
    tab.column_abs('Syst (%)')
    tab.output(tabname, tabprefix=tabprefix)


def doubletageff(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')
    tab.column_append(get_generated_numbers('double', label=tabprefix), 'Generated')
    tab.column_append_from_files('Signal yield', 'N',  
                                 fitbase, tabprefix, 
                                 's', 'd',  'txt', rnd='1.')
    tab.column_append_by_divide('Efficiency(%)', 
                                'Signal yield', 'Generated', 
                                'Efcy', '.01', 100)
    tab.column_append_from_files('FSR', 'FSR', evtlogbase, tabprefix+'/nofsr',  
                                 's', 'd', 'log', rnd='1.', colName='Value')
    tab.column_append_by_subtract('Generated noFSR', 
                                  'Generated', 'FSR')
    tab.column_append_from_files('Signal yield noFSR', 'N',  
                                 fitbase,  tabprefix+'/nofsr',  
                                 's', 'd',  'txt', rnd='1.')
    tab.column_append_by_divide('Efficiency no FSR(%)', 
                                'Signal yield noFSR', 'Generated noFSR', 
                                'Efcy', '.01', 100)
    tab.column_delete('FSR')
    tab.column_delete('Generated noFSR')
    tab.column_delete('Signal yield noFSR')
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    tab.output(tabname, tabprefix=tabprefix, outputtxt=True) 


def evt_pdl(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    file1 = '/nfs/cleo3/Offline/rel/20050525_MCGEN/data/evt.pdl'
    file2 = '/nfs/cleo3/Offline/rel/20080624_MCGEN/data/evt.pdl'

    selected_particles = {
        'psi(3770)': '$\psi(3770)$',
        'psi(2S)': '$\psi(2S)$',
        'J/psi': '$J/\psi$',
        'D+': '$D^+$',
        'D-': '$D^-$',
        'D0': '$D^0$',
        'anti-D0': '$\\bar{D}^0$', 
        'K+': '$K^+$',
        'K-': '$K^-$',
        'K0': '$K^0$',
        'anti-K0': '$\\bar{K}^0$',
        'anti-K*0': '$\\bar{K}^{*0}$',
        'K_1+' : '$K_{1}^{+}$',
        'K_1-' : '$K_{1}^{-}$',
        'rho+' : '$\\rho^{+}$',
        'rho-' : '$\\rho^{-}$',
        'rho0' : '$\\rho^{0}$',
        'a_1+' : '$a_1^+$',
        'a_1-' : '$a_1^-$',
        'a_10' : '$a_1^0$',
        'eta'  : '$\eta$',
        'eta(2S)' : '$\eta(2S)$',
        'pi+' : '$\pi^+$',
        'pi-' : '$\pi^-$',
        'pi0' : '$\pi^0$',
        'omega' : '$\omega$',
        'f_0' : '$f_0$',
        'f_2' : '$f_2$',
        'phi': '$\phi$'}
            
    p1 = PDLFile(file1)
    names_p1 = set(p1.pnames)
    p2 = PDLFile(file2)
    names_p2 = set(p2.pnames)
    names_inter = names_p1 & names_p2
    names_mass_or_width = []
    masses1 = []
    masses2 = []
    widths1 = []
    widths2 = []
    for name in names_inter:
        if selected_particles and name not in selected_particles:
            continue
        mass1 = p1.particles[name]['mass']
        mass2 = p2.particles[name]['mass']
        width1 = p1.particles[name]['width']
        width2 = p2.particles[name]['width']
        if mass1 != mass2 or width1 != width2:
            names_mass_or_width.append(name)
            masses1.append(mass1)
            masses2.append(mass2)
            widths1.append(width1)
            widths2.append(width2)
            
    tab.column_append(names_mass_or_width, 'Name')
    tab.column_append(masses1, 'Mass(Original)')
    tab.column_append(masses2, 'Mass(Default)')
    tab.column_append_by_diff_pct('Mass diff(%)', 'Mass(Default)',
                                  'Mass(Original)')
    tab.column_append(widths1, 'Width(Original)')
    tab.column_append(widths2, 'Width(Default)')
    tab.column_append_by_diff_pct('Width diff(%)',
                                  'Width(Default)', 'Width(Original)')

    tab.column_replace_by_translation('Name', selected_particles)
    tab.output(tabname)


def extlabsbkg(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.row_append(['From', 'To', 'Raw sideband yield',
                    'Corrected background', 'Final'])


    label = tabprefix.replace('dir_', '')

    for mode in [202, 203, 204]:
        bkgname = modes[mode]['bkg_multipions']
        modename = modes[mode]['fname']
        yldprefix = tabprefix+'/kssideband'
        if mode in (202, 203):
            yldprefix += '/fix_sigmap1'

        yldfile = tools.set_file('txt', 'data', mode, 'single',
                                 prefix=yldprefix, extbase=attr.fitpath)
        t = DHadCBXTable(yldfile)
        yld_val = t.cell_get('N1', 'Value')
        yld_err = t.cell_get('N1', 'Error')
        sideband_yld = '%s +/- %s' % (yld_val, yld_err)

        # if tabprefix == 'dir_281ipbv7':
        #     print sideband_yld 
        #     continue

        # if mode == 202:
        #     factor = 0.929296#0.964
        # if mode == 203:
        #     factor =  0.717409
        # if mode == 204:
        #     factor =  0.786769#0.887
        
        Matrix = get_eff_matrix_sideband(mode, label)#, bkg_sb_factor=factor)

        Yld_data = get_yld_vector_sideband('data', mode, label)

        Yld_generic = get_yld_vector_sideband('generic', mode, label)

        absbkg_data = get_corrected_abs_bkg(Matrix, Yld_data)
        
        absbkg_generic = get_corrected_abs_bkg(Matrix, Yld_generic)#, factor)
        absbkg_generic_mctruth = get_generic_mctruth(mode, label)

        print absbkg_generic, absbkg_generic_mctruth
        
        data_val = float(absbkg_data.split('+/-')[0])
        generic_val = float(absbkg_generic.split('+/-')[0])
        fraction = abs(generic_val - absbkg_generic_mctruth
                       )/absbkg_generic_mctruth
        gen_err = data_val * fraction
        absbkg_data = '%s +/- %s' % (absbkg_data, gen_err)
        final_bkg = t.cell_trim(absbkg_data, err_type='Combined', rnd='.1')
        tab.row_append([bkgname, modename, sideband_yld, absbkg_data, final_bkg])
        
    if tabprefix == 'dir_281ipbv7':
        return
    
    for col in [ 'Raw sideband yield', 'Corrected background']:
        tab.column_trim(col, rnd='1')

    tab.column_replace('From', ['From', '$\Dp\\to\pip\pim\pip$',
                                '$\Dp\\to\pip\pim\pip\piz$',
                                '$\Dp\\to 3\pip 2\pim$'])
    tab.column_replace('To', ['To', '$\Dp\\to\KS\pip$',
                              '$\Dp\\to\KS\pip\piz$',
                              ' $\Dp\\to\KS\pip\pip\pim$'])
    tab.output(tabname, tabprefix=tabprefix, outputtxt=True)


def extlabsbkg_generic(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.row_append(['From', 'To', 'bkg in ks sideband region',
                    'bkg in ks signal region', 'correction factor'])
    label = tabprefix.replace('dir_', '')

    for mode in [202, 203, 204]:
        bkgname = modes[mode]['bkg_multipions']
        modename = modes[mode]['fname']
        t = DHadCBXTable()
        absbkg_generic_mctruth = get_generic_mctruth(mode, label)
        evtlabel = label + '/kssideband'
        absbkg_generic_sideband_mctruth = get_generic_mctruth(mode, evtlabel)
        factor = float(absbkg_generic_mctruth)/absbkg_generic_sideband_mctruth
        factor = t.cell_trim(factor, rnd='.001')
        tab.row_append([bkgname, modename, absbkg_generic_mctruth,
                        absbkg_generic_sideband_mctruth, factor])

    tab.output()#tabname, tabprefix=tabprefix, outputtxt=True)


def fitResultsData(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)

    tab = DHadCBXTable()
    tab.column_append(parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(parse_result(bffile, 'value'), 'value')
    tab.column_append(parse_result(bffile, 'stat'),  'stat')
    tab.column_append(parse_result(bffile, 'syst'),  'syst')
    tab.columns_join3('Fitted Value', 'value', 'stat',  'syst')
    tab.column_trim('Fitted Value', row = ['ND0D0Bar', 'ND+D-'],
                    rnd = '.001', factor = 0.000001, opt = '(cell)x10E6')
    tab.column_trim('Fitted Value', rnd = '.00001',
                    except_row = ['ND0D0Bar', 'ND+D-'])
    tab.column_append(parse_result(bffile, 'err_frac'),
                      'Frac. Err', rnd = '.1', opt = '(cell%)')
    tab.columns_join('Fitted Value','Fitted Value','Frac. Err', str=' ')
    tab.column_append(attr.PDG2004_NBF, 'PDG 2004')
    tab.column_append_by_diff_sigma('Difference', 'Fitted Value', 'PDG 2004')
    tab.output(tabname, trans_dict=attr.NBF_dict, tabprefix=tabprefix)


def fitResultsDataVariations(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab = DHadCBXTable()
    bf_A_list = ['nofsr', 'widede', 'gamma/0.0227', 'gamma/0.0277', 'p/0.5']
    bf_B = tabprefix.replace('dir_', '')
    bffile_B = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab.column_append(parse_result(bffile_B, 'paras+ratio'),'Parameters')
    tab.column_append(parse_result(bffile_B, 'value_err+ratio'), bf_B)
    for bf_A in bf_A_list:
        prefix_A = os.path.join(tabprefix, bf_A)
        bffile_A = tools.set_file(
            extbase=attr.brfpath, prefix=prefix_A, comname=bffilename)
        tab.column_append(parse_result(bffile_A,'value_err+ratio'),'tmp')
        tab.column_append_by_diff_sigma_pct(bf_A, 'tmp', bf_B, rnd='.1',
                                            err_type='Indp', opt='%(')
        tab.column_delete('tmp')
    tab.column_delete(bf_B)
    tab.row_hline('BrD2KKPi')
    texhead = r'''Parameter & No FSR & $2\times\Delta E$ & $\Gamma=22.7$ MeV & $\Gamma=27.7$ MeV & $p=0.5$'''
    tab.output(tabname, texhead, trans_dict=attr.NBF_BF_Ratio_dict)


def fitResultsDataVariations1(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab = DHadCBXTable()
    bf_A_list = ['nofsr', 'widede', 'p/0.5']
    bf_B = tabprefix.replace('dir_', '')
    bffile_B = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab.column_append(parse_result(bffile_B, 'paras+ratio'),'Parameters')
    tab.column_append(parse_result(bffile_B, 'value_err+ratio'), bf_B)
    for bf_A in bf_A_list:
        prefix_A = os.path.join(tabprefix, bf_A)
        bffile_A = tools.set_file(
            extbase=attr.brfpath, prefix=prefix_A, comname=bffilename)
        tab.column_append(parse_result(bffile_A,'value_err+ratio'),'tmp')
        tab.column_append_by_diff_sigma_pct(bf_A, 'tmp', bf_B, rnd='.01',
                                            err_type='Indp', opt='%(')
        tab.column_delete('tmp')
    tab.column_delete(bf_B)
    tab.row_hline('BrD2KKPi')
    texhead = r'''Parameter & No FSR & $2\times\Delta E$ & $p=0.5$'''
    tab.output(tabname, texhead, trans_dict=attr.NBF_BF_Ratio_dict,
               tabprefix=tabprefix)


def fitResultsDataVariations2(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab = DHadCBXTable()
    bf_A_list = ['gamma/0.0227', 'gamma/0.0277']
    bf_B = tabprefix.replace('dir_', '')
    bffile_B = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab.column_append(parse_result(bffile_B, 'paras+ratio'),'Parameters')
    tab.column_append(parse_result(bffile_B, 'value_err+ratio'), bf_B)
    for bf_A in bf_A_list:
        prefix_A = os.path.join(tabprefix, bf_A)
        bffile_A = tools.set_file(
            extbase=attr.brfpath, prefix=prefix_A, comname=bffilename)
        tab.column_append(parse_result(bffile_A,'value_err+ratio'),'tmp')
        tab.column_append_by_diff_sigma_pct(bf_A, 'tmp', bf_B, rnd='.01',
                                            err_type='Indp', opt='%(')
        tab.column_delete('tmp')
    tab.column_delete(bf_B)
    tab.row_hline('BrD2KKPi')
    texhead = r'''Parameter & $\Gamma=22.7$ MeV & $\Gamma=27.7$ MeV '''
    tab.output(tabname, texhead, trans_dict=attr.NBF_BF_Ratio_dict)



def fitResultsRatiosData(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)

    tab = DHadCBXTable()
    tab.column_append(parse_result(bffile, 'para_bf_ratio'),
                      'Parameters')

    tab.column_append(parse_result(bffile, 'value_bf_ratio'),
                      'value')
    tab.column_append(parse_result(bffile, 'stat_bf_ratio'),
                      'stat')
    tab.column_append(parse_result(bffile, 'syst_bf_ratio'),
                      'syst')
    tab.columns_join3('Fitted Value','value','stat','syst', rnd='.001')
    tab.column_append(attr.PDG2004_BF_Ratio, 'PDG 2004')
    tab.column_append_by_diff_sigma('Difference', 'Fitted Value', 'PDG 2004')
    
    tab.output(tabname, trans_dict=attr.BF_Ratio_dict, tabprefix=tabprefix)
    

def fitResultsMC(opts, tabname, tabprefix):
    bffilename = 'bf_stat'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)

    tab = DHadCBXTable()
    tab.column_append(parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(parse_result(bffile, 'value_err'), 'Fitted Value')
    if '818ipb' in tabprefix:
         tab.column_append(attr.Generic818_NBF, 'Generated Value')
    if '281ipbv0' in tabprefix:
         tab.column_append(attr.Generic281v0_NBF, 'Generated Value')
         
    tab.column_append_by_diff_sigma('Difference', 'Fitted Value',
                                    'Generated Value')

    if '818ipb' in tabprefix:
         tab.column_trim('Fitted Value', row = ['ND0D0Bar', 'ND+D-'],
                         rnd = '.001', factor = 0.0000001, opt = '(cell)x10E7')
    if '281ipb' in tabprefix:
         tab.column_trim('Fitted Value', row = ['ND0D0Bar', 'ND+D-'],
                         rnd = '.001', factor = 0.000001, opt = '(cell)x10E6')

    tab.column_trim('Fitted Value', rnd = '.00001',
                    except_row = ['ND0D0Bar', 'ND+D-'])
    tab.column_append(parse_result(bffile, 'err_frac'),
                      'Frac. Err', rnd = '.1', opt = '(cell%)')
    tab.columns_join('Fitted Value','Fitted Value','Frac. Err', str=' ')

    if '818ipb' in tabprefix:
         tab.column_trim('Generated Value', row = ['ND0D0Bar', 'ND+D-'],
                         rnd = '.001', factor = 0.0000001, opt = 'cellx10E7')
    if '281ipb' in tabprefix:
         tab.column_trim('Generated Value', row = ['ND0D0Bar', 'ND+D-'],
                         rnd = '.001', factor = 0.000001, opt = 'cellx10E6')
         
    tab.output(tabname, trans_dict=attr.NBF_dict, tabprefix=tabprefix)


def grand_comparison(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tabbase = os.path.join(attr.base, '9.03', 'tab/')
    tabfile = 'compare_yields_signal_7.06.txt'
    comname = tabbase + 'compare_yields_signal_7.06_regular'
    tab.column_append_from_tab_file('Mode', tabbase + tabfile, 'Mode')
    tab.column_append_from_tab_file('Default', tabbase + tabfile, 'diff(%)')
    tab.column_append_from_tab_file('Pass2', comname + '1.txt', 'diff(%)')
    tab.column_append_from_tab_file('4Vec',  comname + '4.txt', 'diff(%)')
    tab.column_append_from_tab_file('DEC', comname + '2.txt', 'diff(%)')
    tab.column_append_from_tab_file('EBeam', comname + '3.txt', 'diff(%)')
    tab.column_append_from_tab_file('PDL&DEC', comname + '5.txt', 'diff(%)')
    tab.column_append_from_tab_file('EvtGen', comname + '8.txt','diff(%)')
    tab.column_append_from_tab_file('LineShape', comname + '11.txt','diff(%)')
    tab.column_append_from_tab_file('Factor', comname + '12.txt','diff(%)')
    tab.column_append_from_tab_file('EvtFac', comname + '13.txt','diff(%)')
    tab.row_append_by_square_sum(name='\chi^2', opt='chisq')
    means = ['Mean']
    sigmas = ['Sigma']
    comname = 'deviations_compare_yields_signal_7.06'
    tabnames = ['', '_regular1', '_regular4', '_regular2',
                '_regular3', '_regular5', '_regular8',
                '_regular11', '_regular12', '_regular13']
    for tn in tabnames:
        tabfile = tabbase + comname + tn + '.org'
        tab_ = DHadCBXTable(tabfile)
        mean =  tab_.get_val_err_by_name('Mean', rnd='.01')
        means.append(mean)
        sigma =  tab_.get_val_err_by_name('Sigma', rnd='.01')
        sigmas.append(sigma)
    tab.row_append(means)
    tab.row_append(sigmas)
    tab.output(tabname)


def kssidebandeff(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.row_append(['Mode', 'Eff'])

    dt_type = 'signal'
    tag = 'single'
    prefix = '%s/kssideband' %tabprefix

    for mode in [202, 203, 204]: 
        modename = modes[mode]['fname']
        tabfile = tools.set_file('txt', dt_type, mode, tag,
                                 prefix=prefix, extbase=attr.fitpath)
        t = DHadCBXTable(tabfile)
        yld_val = t.cell_get('N1', 'Value')
        yld_err = t.cell_get('N1', 'Error')

        gen = get_generated_numbers('single', mode=mode)[0]
        eff_val = float(yld_val)/float(gen)
        eff_err = float(yld_err)/float(gen)
        eff = '%s +/- %s' % (eff_val, eff_err)

        tab.row_append([modename, eff])

    tab.column_trim('Eff', rnd='.1', factor=1000)
    texhead = r'''Mode & $E_{sig\to sb}~ (10^{-3})$'''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)


def lineshapeparameters(opts, tabname, tabprefix):
    prefix = '%s/resolution' %tabprefix
    dt_type = 'signal'
    tag = 'double'

    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname')     
    tab.column_append_from_files(
        'sigma (MeV)', 'sigmacommon1', fitbase, prefix, 
        dt_type, tag,  'txt', rnd='.01', factor=1000)
    tab.column_append_from_files('fa', 'f1a',  fitbase, prefix, 
                                 dt_type, tag,  'txt', rnd='.001')
    tab.column_append_from_files('fb', 'f1b', fitbase, prefix, 
                                 dt_type, tag,  'txt', rnd='.0001')
    tab.column_append_from_files('sa', 's1a',  fitbase, prefix, 
                                 dt_type, tag,  'txt', rnd='.01')
    tab.column_append_from_files('sb', 's1b',  fitbase, prefix, 
                                 dt_type, tag,  'txt', rnd='.01')
    texhead = r'''Mode & $\sigma \rm{(MeV)}$  & $f_a$ & $f_b$ & $s_a$ & $s_b$'''
    tab.output(tabname, texhead, tabprefix=tabprefix)


def mode_dependent_syst(opts, tabname, tabprefix):
    label = tabprefix.replace('dir_', '')
    outtabprefix = tabprefix
    if label == '818ipbv12.4':
        tabprefix = 'dir_818ipbv12'
        signal_shape_prefix = 'dir_818ipbv12.4'
    else:
        signal_shape_prefix = tabprefix
        

    tab = DHadCBXTable()
    modenames = [modes[mode]['sname'] for mode in modes]
    modenames.insert(0, 'Source')
    tab.row_append(modenames)
    tab.row_append(mode_syst_bkg_shape(tabprefix))
    tab.row_append(mode_syst_tracking(tabprefix))
    #tab.row_append(mode_syst_tracking_kaon(tabprefix))
    tab.row_append(mode_syst_ks(tabprefix))
    tab.row_append(mode_syst_pi0(tabprefix))
    tab.row_append(mode_syst_pid_pion(tabprefix))
    tab.row_append(mode_syst_pid_kaon(tabprefix))
    tab.row_append(mode_syst_lepton_veto(tabprefix))
    tab.row_append(mode_syst_fsr(tabprefix))
    tab.row_append(mode_syst_de(tabprefix))
    tab.row_append(mode_syst_signal_shape(signal_shape_prefix))
    tab.row_append(mode_syst_substructure(tabprefix))
    tab.row_append(mode_syst_multcand(tabprefix))

    texhead = r'''Source & $K\pi$ & $K\pi\pi^0$ & $K\pi\pi\pi$ & $K\pi\pi$ & $K\pi\pi\pi^0$ & $K_S^0\pi$ & $K_S^0\pi\pi^0$ & $K_S^0\pi\pi\pi$ & $KK\pi$ '''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=outtabprefix)


def mode_syst_bkg_shape(tabprefix):
    tabdir = tabprefix.replace('dir_', '')
    tabname = 'vary_argus_single.txt'
    tabfile = os.path.join(cbxtabpath, tabdir, tabname)
    tab = DHadCBXTable(tabfile)
    colname = 'max-diff(%)'
    tab.rows_join_by_max(colname)
    syst = tab.column_get(colname)
    syst[0] = 'Bkgd shape'
    syst = [sy.replace('-', '') for sy in syst] 
    return syst


def mode_syst_tracking(tabprefix):
    syst = ['Tracking']
    per_pion = 0.3
    per_kaon = 0.6
    for mode in modes:
        daughters = modes[mode]['daughter_defs']
        sy = '--' 
        for dau in daughters.values():
            if dau == 'pi+' or dau == 'pi-':
                if sy == '--':
                    sy = per_pion
                else:
                    sy += per_pion
                    
            if dau == 'K+' or dau == 'K-':
                if sy == '--':
                    sy = per_kaon
                else:
                    sy += per_kaon

            if '818ipbv12.7' in tabprefix: 
                if dau == 'KS': 
                    if sy == '--':
                        sy = 2*per_pion
                    else:
                        sy += 2*per_pion
                    
        syst.append(sy)
    return syst


def mode_syst_tracking_pion(tabprefix):
    syst = ['pion tracking']
    per_pion = 0.3
    for mode in modes:
        daughters = modes[mode]['daughter_defs']
        sy = '--' 
        for dau in daughters.values():
            if dau == 'pi+' or dau == 'pi-':
                if sy == '--':
                    sy = per_pion
                else:
                    sy += per_pion
        syst.append(sy)
    return syst


def mode_syst_tracking_kaon(tabprefix):
    syst = ['K tracking']
    for mode in modes:
        syst.append(0.6)
        if mode in [205]:
            syst.append(1.2)
    return syst


def mode_syst_ks(tabprefix):
    syst = ['KS0']
    for mode in modes:
        if mode in [202, 203, 204]:
            syst.append(0.8)
        else:
            syst.append('--')
    return syst


def mode_syst_pi0(tabprefix):
    tabdir = tabprefix.replace('dir_', '')
    tabname = 'pi0_eff_correction.txt'
    tabfile = os.path.join(cbxtabpath, tabdir, tabname)
    tab = DHadCBXTable(tabfile)
    colname = 'eff_data/eff_MC'
    tab.column_trim(colname, err_type='Only', factor=100)
    pi0_modes = tab.column_get('Mode')
    syst = ['pi0']
    for mode in modes:
        modename = modes[mode]['fname']
        if modename in pi0_modes:
            syst.append(tab.cell_get(modename, colname))
        else:
            syst.append('--')
    return syst


def mode_syst_pid_pion(tabprefix):
    syst = ['pi PID']
    per_pion = 0.25
    
    for mode in modes:
        daughters = modes[mode]['daughter_defs']
        sy = '--' 
        for dau in daughters.values():
            if dau == 'pi+' or dau == 'pi-':
                if sy == '--':
                    sy = per_pion
                else:
                    sy += per_pion
        syst.append(sy)
    return syst


def mode_syst_pid_kaon(tabprefix):
    syst = ['K PID']
    per_kaon = 0.3
    
    for mode in modes:
        daughters = modes[mode]['daughter_defs']
        sy = '--' 
        for dau in daughters.values():
            if dau == 'K+' or dau == 'K-':
                if sy == '--':
                    sy = per_kaon
                else:
                    sy += per_kaon
        syst.append(sy)
    return syst


def mode_syst_lepton_veto(tabprefix):
    syst = ['Lepton veto']
    for mode in modes:
        if mode == 0:
            syst.append(0.1)
        else:
            syst.append('--')
    return syst

def mode_syst_fsr(tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tabfile = os.path.join(cbxtabpath, 'singletag_sigmc_eff_nofsr.txt')
    name = 'FSR'
    tab.column_append_from_tab_file('FSR_ratio', tabfile, 'Ratio')
    tab.column_append_by_subtract_number('FSR_shift', 'FSR_ratio', 1)
    tab.column_append_by_times_number(name, 'FSR_shift', 25, rnd='.1')
    tab.rows_join_by_max(name)
    tab.column_trim('FSR', err_type='None')
    return tab.column_get(name)


def mode_syst_de(tabprefix):
    tabdir = tabprefix.replace('dir_', '')
    tabname = 'singletag_de_syst.txt'
    tabfile = os.path.join(cbxtabpath, tabdir, tabname)
    tab = DHadCBXTable(tabfile)
    colname = 'Syst (%)'
    syst = tab.column_get(colname)
    syst[0] = 'Delta E (*)'
    return syst


def mode_syst_signal_shape(tabprefix):
    tabdir = tabprefix.replace('dir_', '')
    tabname = 'signal_line_shape_syst.txt'
    tabfile = os.path.join(cbxtabpath, tabdir, tabname)
    tab = DHadCBXTable(tabfile)
    colname = 'Total(%)'
    syst = tab.column_get(colname)
    syst[0] = 'Signal shape'
    return syst


def mode_syst_substructure(tabprefix):
    tabdir = tabprefix.replace('dir_', '')
    tabname = 'resonant_syst.txt'
    tabfile = os.path.join(cbxtabpath, tabdir, tabname)
    tab = DHadCBXTable(tabfile)
    colname = 'max (%)'
    syst = tab.column_get(colname)
    # tabfile_kkpi = os.path.join(cbxtabpath, tabdir, 'syst_kkpi.txt')
    # tab_kkpi = DHadCBXTable(tabfile_kkpi)
    # tab_kkpi.output()
    # syst_kkpi = tab_kkpi.column_get('max-diff(%)')
    # syst_kkpi = max(syst_kkpi[1], syst_kkpi[2])
    syst_kkpi = 0.99
    syst[-1] = syst_kkpi
    syst[0] = 'Substructure (*)'
    return syst


def mode_syst_multcand(tabprefix):
    tabdir = tabprefix.replace('dir_', '')
    if tabdir == '818ipbv12':
        tabdir = '818ipbv7' # used the same Generic MC to calcuate

    tabname = 'syst_multcand.txt'
    tabfile = os.path.join(cbxtabpath, tabdir, tabname)
    tab = DHadCBXTable(tabfile)
    colname = 'Error (%)'
    syst = tab.column_get(colname)
    syst[0] = 'Mult. cand. (*)'
    return syst


def pi0_eff_correction(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    row = ['Mode', 'Average pi0 momentum', 'eff_data/eff_MC']
    tab.row_append(row)

    for mode in [1, 201, 203]: 
        modename = modes[mode]['fname']
        p_avg = modes[mode]['average pi0 momentum']
        ratio = get_pi0_eff_correction(p_avg)
        tab.row_append([modename, p_avg, ratio])        

    tab.column_trim('eff_data/eff_MC', rnd='.001')
    texhead = r'''Mode & Average $\pi^0$ momentum  & $\epsilon_{data}/\epsilon_{MC}$''' 
    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)
    

def resonant_syst(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    label = tabprefix.replace('dir_', '')
       
    tab.row_append(['Mode', 'dau1(%)', 'dau2(%)',
                    'dau3(%)', 'dau4(%)', 'max (%)'])

    for mode in modes:
        modename = modes[mode]['fname']
        sname =  modes[mode]['sname'].lower()
        tabfile = os.path.join(attr.tabpath, label, '%s_syst.txt' %sname)
        if not os.access(tabfile, os.F_OK):
            row = [modename, '--', '--', '--', '--', '--']
            tab.row_append(row)
            continue
        tmptab = DHadCBXTable(tabfile)
        tmpcol = tmptab.column_get('Data/MC')
        row = [abs(1-eval(cell))*100 for cell in tmpcol[1:] ]
        row_max = max(row)
        if len(row) == 3:
            row.append('--')
        row.append(row_max)
        row.insert(0, modename)
        tab.row_append(row)
        
    tab.output(tabname, outputtxt=True, tabprefix=tabprefix)

def reweight_results(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.row_append(['Mode', 'Track +', 'Track -', 'pi0 +', 'pi0 -'])
    label = tabprefix.replace('dir_', '')
    for mode in modes:
        modename = modes[mode]['fname']
        trk_inc, pi0_inc = get_multspec_reweight('inc', 'signal',
                                                 'Single_'+modename, label)
        trk_dec, pi0_dec = get_multspec_reweight('dec', 'signal',
                                                 'Single_'+modename, label)
        tab.row_append([modename,trk_inc, trk_dec, pi0_inc, pi0_dec])

    for col in ['Track +', 'Track -', 'pi0 +', 'pi0 -']:
        tab.column_trim(col, rnd='.0001', opt='+/-')
        
    texhead = r'''Mode  & Track $+$ & Track $-$ & $\pi^0~ +$ & $\pi^0~-$'''
    tab.output(tabname, texhead, tabprefix=tabprefix)
    

def signal_line_shape_syst(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tabdir = ''
    outtabprefix = tabprefix
    additional_syst = None
    if tabprefix == 'dir_818ipbv12.4':
        tabprefix = 'dir_818ipbv12'
        additional_syst = 0.004
    if 'dir_' in tabprefix:
        tabdir = tabprefix.replace('dir_', '')
        
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tab_file_A = os.path.join(cbxtabpath, tabdir, 'vary_mass_single.txt')
    name_A  = 'Mass(+/-0.5 MeV)%'
    column = 'max-diff(%)'
    tab.column_append_from_tab_file(name_A, tab_file_A, column)

    tab_file_B = os.path.join(cbxtabpath, tabdir, 'vary_width_single.txt')
    name_B  = 'Gamma(+/-2.5 MeV)%'
    tab.column_append_from_tab_file(name_B, tab_file_B, column)

    tab_file_C =  os.path.join(cbxtabpath, tabdir, 'vary_R_single.txt')
    name_C  = 'R(+/- 4)%'
    tab.column_append_from_tab_file(name_C, tab_file_C, column)

    name_D = 'Total(%)'
    tab.column_append_by_add_quadrature3(name_D, name_A,
                                        name_B, name_C, rnd='.01')
    
    tab.rows_join_by_max(name_D)

    if additional_syst != None:
        name_E = 'With additional %s (%)'
        tab.column_append(['add', 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4])
        tab.column_append_by_add_quadrature('TMP', 'add', name_D,  rnd='.01')
        tab.columns_delete(['Total(%)', 'add'])
        new_tot =  tab.column_get('TMP')
        new_tot[0] ='Total(%)' 
        tab.column_replace('TMP', new_tot)
    
    texhead = r'''Mode  & \multicolumn{3}{c}{Difference(\%)} & Total \\
    & Mass$(\pm~0.5)$ MeV	 & $\Gamma(\pm~2.5)$ MeV & $R(\pm~4~ \rm{GeV}^{-1})$ & (\%) '''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=outtabprefix)



def singletag_data_yield(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    bkgprefix = tabprefix

    if '.' in tabprefix:
        tabprefix = tabprefix.split('.')[0]
        
    tab.column_append_from_dict('Mode', 'fname,fnamebar')     
    tab.column_append_from_files('Gamma 22.7 MeV', 'N1,N2',  
                                 fitbase, tabprefix+'/gamma/0.0227',  
                                 'd', 's', 'txt', rnd='1.')
    tab.column_append_from_files('Gamma 25.2 MeV', 'N1,N2',  
                                 fitbase, tabprefix,  
                                 'd', 's', 'txt', rnd='1.')
    tab.column_append_from_files('Gamma 27.7 MeV', 'N1,N2',  
                                 fitbase, tabprefix+'/gamma/0.0277',  
                                 'd', 's', 'txt', rnd='1.')
    tab.column_append_from_files('D mass (MeV)', 'md,md',  
                                 fitbase, tabprefix,  
                                 'd', 's', 'txt', 
                                 rnd='0.001', factor= 1000)
    tab.column_append(data_bkg_single(opts, bkgprefix), 'Bkgd')
    tab.column_trim('Bkgd', rnd = '1.', err_type='<1')

    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & $D$ mass (MeV) & Bkg \\
& $\Gamma = 22.7$ MeV & $\Gamma = 25.2$ MeV & $\Gamma = 27.7$ MeV '''

    tab.output(tabname, texhead, tabprefix=bkgprefix, outputtxt=True)

   
def singletag_data_yield_pstudy(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tab.column_append_from_files('Yield1(regular)', 'N1,N2', fitbase,
                                 tabprefix, 'd', 's', 'txt', rnd='1.')
    tab.column_append_from_files('Yield2(p=0.5)', 'N1,N2',  fitbase, 
                                 tabprefix+'/p/0.5', 'd', 's', 'txt', rnd='1.')
    tab.column_append_by_divide('Yield1/Yield2', 'Yield1(regular)', 
                                'Yield2(p=0.5)', 'Efcy', '.0001') 
    tab.column_append_from_files('eff1(regular)', 'N1,N2', fitbase,
                                 tabprefix, 's', 's', 'txt', rnd='1.')
    tab.column_append_from_files('eff2(p=0.5)', 'N1,N2', fitbase,
                                 tabprefix+'/p/0.5', 's', 's', 'txt', rnd='1.')
    tab.column_append_by_divide('eff1/eff2',  'eff1(regular)', 
                                'eff2(p=0.5)', 'Efcy', '.0001') 
    tab.column_append_by_divide('Ratio',  'Yield1/Yield2', 
                                 'eff1/eff2', 'Indp', '.0001') 
    tab.columns_delete(['Yield1(regular)','Yield2(p=0.5)', 
                        'eff1(regular)','eff2(p=0.5)' ])
    tab.output(tabname, tabprefix=tabprefix)

    
def singletag_data_yield_widede(opts, tabname, tabprefix):
    tab = DHadCBXTable()
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
    tab.column_append_from_files('eff1(noFSR)', 'N1,N2', fitbase,
                                 tabprefix+'/nofsr', 's', 's', 'txt', rnd='1.')
    tab.column_append_from_files('eff2(widede_noFSR)', 'N1,N2',  fitbase,
                                 tabprefix+'/widede/nofsr', 's', 's', 'txt',
                                 rnd='1.')
    tab.column_append_by_divide('eff1(noFSR)/eff2(widede_noFSR)',
                                'eff1(noFSR)', 'eff2(widede_noFSR)', 
                                'Efcy', '.001') 
    tab.columns_delete(['Yield1(regular)', 'Yield2(widede)', 'eff1(regular)',
                        'eff2(widede)', 'eff1(noFSR)', 'eff2(widede_noFSR)'])
    
    texhead = r'''Mode	 & Yield1/Yield2  & eff1/eff2 & Ratio & eff1'/eff2' '''
    tab.output(tabname, texhead, tabprefix=tabprefix)


def singletag_de_syst(opts, tabname, tabprefix):
    tab = DHadCBXTable()
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
    tab.columns_delete(['Yield1(regular)', 'Yield2(widede)', 'eff1(regular)',
                        'eff2(widede)', 'Yield1/Yield2', 'eff1/eff2'])
    tab.column_append_by_subtract_number('Syst (%)', 'Ratio', '1',
                                         rnd='.01', factor=100, err_type='None')
    tab.rows_join_by_max('Syst (%)')
    tab.column_abs('Syst (%)')
    tab.output(tabname, outputtxt=True, tabprefix=tabprefix)


def singletag_sigmc_eff(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tab.column_append(get_generated_numbers('single', label=tabprefix),
                      'Generated')
    tab.column_append_from_files('Yield', 'N1,N2', fitbase, tabprefix, 
                                 's', 's' ,'txt', rnd='1.')
    tab.column_append_from_files('mass', 'md,md', fitbase, tabprefix, 
                                 's', 's' ,'txt', rnd = '.001', factor=1000)
    tab.column_append_from_files('$\\xi$', 'xi,xi', fitbase, tabprefix, 
                                 's', 's' ,'txt', rnd = '.1')
    tab.column_append_from_files('p', 'p,p', fitbase, tabprefix, 
                                 's', 's' ,'txt',rnd = '.01')
    tab.column_append_by_divide('Efficiency(%)','Yield','Generated',  
                                'Efcy', '.01', 100) 
    tab.output(tabname, outputtxt=True, tabprefix=tabprefix)


def singletag_sigmc_eff_nofsr(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    tab.column_append(get_generated_numbers('single'), 'Generated')
    tab.column_append_from_files('FSR', 'FSR', evtlogbase,
                                 tabprefix+'/nofsr', 's', 's', 'log', 
                                 sign='1,-1', colName='Value') 
    tab.column_append_by_subtract('Generated without FSR',
                                  'Generated', 'FSR')    
    tab.column_append_by_divide('Gen# noFSR/Regular', 'Generated without FSR',
                                'Generated', 'Bino', '.0001')
    tab.column_append_from_files('Regular Yield', 'N1,N2', fitbase, tabprefix, 
                                 's', 's', 'txt', rnd='1.')
    tab.column_append_from_files('Yield without FSR', 'N1,N2', fitbase,  
                                 tabprefix+'/nofsr', 's', 's', 'txt', rnd='1.')
    tab.column_append_by_divide('Yield noFSR/Regular', 'Yield without FSR', 
                                'Regular Yield', 'Bino', '.0001') 
    tab.column_append_by_divide('Ratio with Error', 'Gen# noFSR/Regular', 
                                'Yield noFSR/Regular', 'Indp', '.0001') 
    tab.column_append_by_divide('Efficiency without FSR(%)',
                                'Yield without FSR', 'Generated without FSR', 
                                'Efcy', '.01', 100)
    tab.column_append_by_divide('Efficiency with FSR(%)', 
                                'Regular Yield', 'Generated', 
                                'Efcy', '.01', 100) 
    tab.column_append_by_divide('Ratio', 'Efficiency without FSR(%)', 
                                'Efficiency with FSR(%)', 'Apnd', '.001',  
                                refCol='Ratio with Error') 
    tab.column_delete('Generated')
    tab.column_delete('FSR')
    tab.column_delete('Generated without FSR')
    tab.column_delete('Regular Yield')
    tab.column_delete('Gen# noFSR/Regular')
    tab.column_delete('Yield noFSR/Regular')
    tab.column_delete('Yield without FSR')
    tab.column_delete('Ratio with Error')
    tab.output(tabname, outputtxt=True, tabprefix=tabprefix)


def syst_kkpi(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    label = tabprefix.replace('dir_', '')
    mode = 205 

    tab.column_append_from_dict('Mode', 'fname,fnamebar', mode=mode)
    tab.column_append(get_generated_numbers('single', mode=mode), 'Generated')
    tab.column_append_from_files('Yield', 'N1,N2', fitbase, tabprefix, 
                                 's', 's' ,'txt', rnd='1.', mode=mode)
    tab.column_append_by_divide('Eff(%)','Yield','Generated',  
                                'Efcy', '.01', 100) 
    tab.columns_delete(['Generated', 'Yield'])

    def get_eff(subdir):
        logname = 'signal_Single_%s.txt' % modes[mode]['fname']
        logpath = os.path.join(attr.logpath, label, subdir, 'yld')
        logfile = tools.set_file(extbase=logpath, comname=logname)
        for line in file(logfile):
            if 'selected' in line:
                total = int(line.split()[-1].replace('.', ''))
                break
        t = DHadCBXTable()
        t.column_append([total, total], 'Generated')
        t.column_append_from_files('Yield', 'N1,N2', fitbase, '%s/%s' %(
            tabprefix, subdir), 's', 's' ,'txt', rnd='1.', mode=mode)
        t.column_append_by_divide('%s(%%)' % subdir, 'Yield','Generated',  
                                  'Efcy', '.01', 100)
        return t.column_get('%s(%%)' % subdir)

    for subdir in ['phipi', 'k0star', 'kstar1410']:
        tab.column_append(get_eff(subdir))
        head_diff =  subdir
        col = '%s(%%)' % subdir
        std = 'Eff(%)'
        tab.column_append_by_diff_pct(head_diff, col, std)

    tab.column_append_by_max('max1', 'phipi', 'k0star')
    tab.column_append_by_max('max-diff(%)', 'max1', 'kstar1410')

    tab.columns_delete(['phipi', 'k0star', 'kstar1410', 'max1'])
    #tab.output(tabname, outputtxt=True, tabprefix=tabprefix)

    effs = tab.row_get('Dp_to_KKpi')[2:5]
    bfs = ['3.20 +/- 0.96', '3.02 +/- 0.91', '3.70 +/- 1.11']

    tab = DHadCBXTable()
    tab.column_append(['Sub Mode', 'phipi', 'k0star', 'kstar1410'])
    tab.column_append(effs, 'Effs (%)')
    tab.column_append(bfs, 'BFs (x10^-3)')
    #tab.output(tabname, outputtxt=True, tabprefix=tabprefix)

#def syst_kkpi_avg(opts, tabname, tabprefix):
#    tab = DHadCBXTable()
#    tab.row_append(['Mode', 'BFs (x10^-3)', 'Effs (%)'])
#    tab.row_append(['phipi', '3.2 +/- 0.4', '43.68 +/- 0.38'])
#    tab.row_append(['k0star', '3.02 +/- 0.35', '45.21 +/- 0.37'])

    
#    tab.row_append(['phsp', '3.7 +/- 0.4', '40.68 +/- 0.34'])
#    tab.output()

    bs = []
    es = []
    ebs = []

    #errfactor = parse_opts_set(opts.set, 'errfactor')

    for m in ['phipi', 'k0star', 'kstar1410']:
        b = tab.cell_get(m, 'BFs (x10^-3)')
        b_parsed = tab.cell_parse(b)
        b_val = b_parsed['value']
        bs.append(float(b_val)*.001)

        e = tab.cell_get(m, 'Effs (%)')
        e_parsed = tab.cell_parse(e)
        e_val = e_parsed['value']
        es.append(float(e_val)*.01)
        
        ebs.append(float(e_val)*0.01*float(b_val)*0.001)
        
    B = sum(bs)
    eff = sum(ebs)/B

    sigmasqs = 0 
    for m in ['phipi', 'k0star', 'kstar1410']:
        b = tab.cell_get(m, 'BFs (x10^-3)')
        b_parsed = tab.cell_parse(b)
        b_val = b_parsed['value']
        b_err = b_parsed['error']

        e = tab.cell_get(m, 'Effs (%)')
        e_parsed = tab.cell_parse(e)
        e_val = e_parsed['value']
        e_err = e_parsed['error']

        bi = float(b_val)*.001
        sigmai = float(b_err)*.001
        #if errfactor != None:
        #     sigmai = float(b_val)* float(errfactor)*.001

        si = float(e_err)*.01
        ei = float(e_val)*.01

        element = ((bi*si)**2 + (ei-eff)**2 * sigmai**2)/(B*B) 

        sigmasqs += element

    sigma_eff = sqrt(sigmasqs)

    syst_err = sigma_eff/eff*100

    tab.column_replace('Sub Mode', ['Sub Mode', '$\phi\pi$', '$K_0^{*}$',
                                     '$\kstar$'])
    texhead = r'''Sub Mode  & Effs (\%) & BFs ($\times 10^{-3}$) '''
    tab.output(tabname, texhead, tabprefix=tabprefix, outputtxt=True)
   
    sys.stdout.write('Eff = %s +/- %s (%s %%) \n' %(eff, sigma_eff, syst_err))


    

def syst_multcand(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.row_append(['Mode', 'F_data(%)', 'F_MC(%)', 'F_MC - F_data (%)',
                    'DeltaE/E_MC(%)', 'Error (%)'])
    label = tabprefix.replace('dir_', '')
    for mode in modes:
        modename = modes[mode]['fname']
        F_data, F_MC, F_Diff, Delta = matrix_inv_cov_epsilon(mode, label)
        Error = tab.cell_min_abs(F_Diff, Delta, threshold=0.002)
        Error = tab.cell_trim(Error, rnd='.1', factor=100)
        tab.row_append([modename, F_data, F_MC, F_Diff, Delta, Error])

    for col in ['F_data(%)', 'F_MC(%)', 'F_MC - F_data (%)', 'DeltaE/E_MC(%)']:
        tab.column_trim(col, rnd='.01', factor=100)

    texhead = r'''Mode  & $F_{\rm data}$ (\%) & $F_{\rm MC}$ (\%) & $F_{\rm MC} - F_{\rm data}$ (\%) & $\Delta\epsilon/\epsilon_{\rm MC}$ (\%) & Error (\%) '''
    tab.output(tabname, texhead, tabprefix=tabprefix, outputtxt=True)


def trigeffs(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname')
    tab.column_append_from_files('Std', 'N1,N2', fitbase, tabprefix,
                                 's', 's', 'txt', rnd='1.')
    tab.column_append_from_files('Trig', 'N1,N2', fitbase, tabprefix+'/trig',
                                 's', 's', 'txt', rnd='1.')
    tab.column_append_by_divide('Trigger efficiency (%)',
                                'Trig', 'Std', 'Efcy', '.001', 100)
    tab.column_trim('Trigger efficiency (%)', err_type='Efcy')
    tab.columns_delete(['Std','Trig'])
    tab.output(tabname, tabprefix=tabprefix)
    
    
def vary_argus_single(opts, tabname, tabprefix):
    tab = DHadCBXTable()
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
    #tab.columns_delete([headA, headB])
    tab.columns_trim(titles, rnd='1.')

#    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
#    & ARGUS Low & Std  & ARGUS High & (\%)  '''
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & diff(low) & diff(high) & max-diff \\
    & ARGUS Low & Std  & ARGUS High & (\%) & (\%) & (\%)  '''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)


def vary_argus_single_generic(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    titles = ['argus_low', 'std', 'argus_high']
    tab.column_append_from_files(titles[0], 'N1,N2', fitbase,
                                 tabprefix+'/argus_low', 'g', 's', 'txt')
    tab.column_append_from_files(titles[1], 'N1,N2', fitbase, tabprefix,  
                                 'g', 's', 'txt')
    tab.column_append_from_files(titles[2], 'N1,N2', fitbase,
                                 tabprefix+'/argus_high', 'g', 's', 'txt')

    std = titles[1]
    colA = titles[0]
    colB = titles[2]
    headA = 'diff(%s)' %colA
    headB = 'diff(%s)' %colB
    headC = 'max-diff(%)'
    tab.column_append_by_diff_pct(headA, colA, std)
    tab.column_append_by_diff_pct(headB, colB, std)
    tab.column_append_by_max(headC, headA, headB)
    tab.columns_trim(titles, rnd='1.')

    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & diff(low) & diff(high) & max-diff \\
    & ARGUS Low & Std  & ARGUS High & (\%) & (\%) & (\%)  '''
    tab.output(tabname, texhead, outputtxt=True)



def vary_mass_double(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')
    titles = ['M_3.7719', 'M_3.7724', 'M_3.7729']
    tab.column_append_from_files(titles[0], 'N', fitbase,
                                 tabprefix+'/mass/3.7719',  
                                 'd', 'd', 'txt')
    tab.column_append_from_files(titles[1], 'N', fitbase, tabprefix,  
                                 'd', 'd', 'txt')
    tab.column_append_from_files(titles[2], 'N', fitbase,
                                 tabprefix+'/mass/3.7729', 'd', 'd', 'txt')
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
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
    & $M=3771.9 $ MeV & $M=3772.4$ MeV & $M=3772.9 $ MeV &(\%)  '''
    tab.output(tabname, texhead, tabprefix=tabprefix)

    
    
def vary_mass_single(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    titles = ['M_3.7719', 'M_3.7724', 'M_3.7729']
    tab.column_append_from_files(titles[0], 'N1,N2', fitbase,
                                 tabprefix+'/mass/3.7719', 'd', 's', 'txt')
    tab.column_append_from_files(titles[1], 'N1,N2', fitbase, tabprefix,  
                                 'd', 's', 'txt')
    tab.column_append_from_files(titles[2], 'N1,N2', fitbase,
                                 tabprefix+'/mass/3.7729', 'd', 's', 'txt')
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
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
    & $M=3771.9 $ MeV & $M=3772.4$ MeV & $M=3772.9 $ MeV &(\%)  '''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)


def vary_mass_single_kedr(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    titles = ['M_3.7724', 'M_3.7779']
    tab.column_append_from_files(titles[0], 'N1,N2', fitbase, tabprefix,  
                                 'd', 's', 'txt')
    tab.column_append_from_files(titles[1], 'N1,N2', fitbase,
                                 tabprefix+'/mass/3.7779', 'd', 's', 'txt')
    std = titles[0]
    colA = titles[1]
    headA = 'diff'
    tab.column_append_by_diff_pct(headA, colA, std)
    tab.columns_trim(titles, rnd='1.')
    texhead = r'''Mode  &  $M=3772.4 $ MeV & $M=3777.9$ MeV & diff (\%)  '''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)

def vary_mass_single_kedr_chisq(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    masses = ['3.7719', '3.7724', '3.7729', '3.7779']
    for mass in masses:
         if mass == '3.7724':
              tab.column_append_from_files(
              'M_%s' %mass, 'N1,N2', fitbase,
                   tabprefix, 'd', 's', 'txt', rnd='1')
              tab.column_append_from_files(
                   'chisq', 'chisq1,chisq2', fitbase,
                   tabprefix, 'd', 's', 'txt')
              
         else:
              tab.column_append_from_files(
                   'M_%s' %mass, 'N1,N2', fitbase,
                   tabprefix+'/mass/%s' %mass, 'd', 's', 'txt', rnd='1')
              tab.column_append_from_files(
                   'chisq', 'chisq1,chisq2', fitbase,
                   tabprefix+'/mass/%s' %mass, 'd', 's', 'txt')
              
         tab.column_trim('chisq', rnd='1', err_type='None',  opt='(cell)')
         tab.columns_join('M_%s (chisq)' %mass, 'M_%s' %mass,
                          'chisq', str='~')
         
         
    texhead = r'''Mode  & \multicolumn{4}{c}{Yield} \\
    & M=3771.9 MeV $(\chi^2)$ & M=3772.4 MeV $(\chi^2)$ & M=3772.9 MeV $(\chi^2)$ & M=3777.9 MeV $(\chi^2)$ '''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)


def vary_mass_single_ext_chisq(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    masses = ['3.7704', '3.7709', '3.7734', '3.7739']
    for mass in masses:
         if mass == '3.7724':
              pass
         else:
              tab.column_append_from_files(
                   'M_%s' %mass, 'N1,N2', fitbase,
                   tabprefix+'/mass/%s' %mass, 'd', 's', 'txt', rnd='1')
              tab.column_append_from_files(
                   'chisq', 'chisq1,chisq2', fitbase,
                   tabprefix+'/mass/%s' %mass, 'd', 's', 'txt')
              
         tab.column_trim('chisq', rnd='1', err_type='None',  opt='(cell)')
         tab.columns_join('M_%s (chisq)' %mass, 'M_%s' %mass,
                          'chisq', str='~')
         
         
    texhead = r'''Mode  & \multicolumn{4}{c}{Yield} \\
    & M=3770.4 MeV $(\chi^2)$ & M=3770.9 MeV $(\chi^2)$ & M=3773.4 MeV $(\chi^2)$ & M=3773.9 MeV $(\chi^2)$ '''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)


def vary_R_double(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')
    titles = ['R_8.7', 'R_12.7', 'R_16.7']
    tab.column_append_from_files(titles[0], 'N', fitbase,
                                 tabprefix+'/r/8.7', 'd', 'd', 'txt')
    tab.column_append_from_files(titles[1], 'N', fitbase, tabprefix,  
                                 'd', 'd', 'txt')
    tab.column_append_from_files(titles[2], 'N', fitbase,
                                 tabprefix+'/r/16.7', 'd', 'd', 'txt')
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
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
    & $R = 8.7 ~ \rm{GeV}^{-1}$ & $R = 12.7 ~ \rm{GeV}^{-1}$ & $R = 16.7 ~ \rm{GeV}^{-1}$ &(\%) '''
    tab.output(tabname, texhead, tabprefix=tabprefix)


def vary_R_single(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    titles = ['R_8.7', 'R_12.7', 'R_16.7']
    tab.column_append_from_files(titles[0], 'N1,N2', fitbase,
                                 tabprefix+'/r/8.7', 'd', 's', 'txt')
    tab.column_append_from_files(titles[1], 'N1,N2', fitbase, tabprefix,  
                                 'd', 's', 'txt')
    tab.column_append_from_files(titles[2], 'N1,N2', fitbase,
                                 tabprefix+'/r/16.7', 'd', 's', 'txt')
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
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
    & $R = 8.7 ~ \rm{GeV}^{-1}$ & $R = 12.7 ~ \rm{GeV}^{-1}$ & $R = 16.7 ~ \rm{GeV}^{-1}$ &(\%) '''

    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)

    
def vary_width_double(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')
    titles = ['G_0.0227', 'G_0.0252', 'G_0.0277']
    tab.column_append_from_files(titles[0], 'N', fitbase,
                                 tabprefix+'/gamma/0.0227', 'd', 'd', 'txt')
    tab.column_append_from_files(titles[1], 'N', fitbase, tabprefix,  
                                 'd', 'd', 'txt')
    tab.column_append_from_files(titles[2], 'N', fitbase,
                                 tabprefix+'/gamma/0.0277', 'd', 'd', 'txt')
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
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
    & $\Gamma = 22.7$ MeV & $\Gamma = 25.2$ MeV & $\Gamma = 27.2$ MeV &(\%) '''
    tab.output(tabname, texhead, tabprefix=tabprefix)


def vary_width_single(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')
    titles = ['G_0.0227', 'G_0.0252', 'G_0.0277']
    tab.column_append_from_files(titles[0], 'N1,N2', fitbase,
                                 tabprefix+'/gamma/0.0227', 'd', 's', 'txt')
    tab.column_append_from_files(titles[1], 'N1,N2', fitbase, tabprefix,  
                                 'd', 's', 'txt')
    tab.column_append_from_files(titles[2], 'N1,N2', fitbase,
                                 tabprefix+'/gamma/0.0277', 'd', 's', 'txt')

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
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    texhead = r'''Mode  & \multicolumn{3}{c}{Yield} & max-diff \\
    & $\Gamma = 22.7$ MeV & $\Gamma = 25.2$ MeV & $\Gamma = 27.2$ MeV &(\%) '''
    tab.output(tabname, texhead, outputtxt=True, tabprefix=tabprefix)
    

   

def yields_comparison(opts, tabname, tabprefix):
    tab = DHadCBXTable()
    tabbase = os.path.join(attr.base, '9.03', 'tab/')
    tabfile = 'compare_yields_signal_7.06.txt'
    comname = tabbase + 'compare_yields_signal_7.06_regular'
    tab.column_append_from_tab_file('Mode', tabbase + tabfile, 'Mode')
    tab.column_append_from_tab_file('Default', comname + '12.txt','diff(%)')
    tab.column_append_from_tab_file('EvtGen', comname + '13.txt','diff(%)')
    tab.column_append_from_tab_file('PdlDec', comname + '14.txt', 'diff(%)')
    tab.column_append_from_tab_file('EBeam', comname + '15.txt', 'diff(%)')
    tab.column_append_from_tab_file('Decay', comname + '16.txt', 'diff(%)')
    tab.row_append_by_square_sum(name='$\chi^2$', opt='chisq')
    means = ['Mean']
    sigmas = ['Sigma']
    comname = 'deviations_compare_yields_signal_7.06'
    tabnames = ['_regular12', '_regular13', '_regular14',
                '_regular15', '_regular16']
    for tn in tabnames:
        tabfile = tabbase + comname + tn + '.org'
        tab_ = DHadCBXTable(tabfile)
        mean =  tab_.get_val_err_by_name('Mean', rnd='.01')
        means.append(mean)
        sigma =  tab_.get_val_err_by_name('Sigma', rnd='.01')
        sigmas.append(sigma)

    tab.row_append(means)
    tab.row_append(sigmas)
    tab.row_hline('Dm_to_KKpi')
    tab.output(tabname)


def yieldDTResidualsData(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')
    tab.column_append(parse_result(bffile, 'residual_double'),
                      'Residual', rnd = '1.')
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    tab.output(tabname, tabprefix=tabprefix)


def yieldDTResidualsMC(opts, tabname, tabprefix):
    bffilename = 'bf_stat'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar', 'double')
    tab.column_append(parse_result(bffile, 'residual_double_mc'),
                      'Residual', rnd = '1.')
    tab.column_append(parse_result(bffile, 'residual_chi2_double_mc'),
                      '$\chi^2$', rnd='0.1')
    tab.row_hline('D0_to_Kpipipi D0B_to_Kpipipi')
    tab.output(tabname, tabprefix=tabprefix)


def yieldSTResidualsData(opts, tabname, tabprefix):
    bffilename = 'bf_stat_sys'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')     
    tab.column_append(parse_result(bffile, 'residual_single'),
                      'Residual', rnd='1.')
    tab.output(tabname, tabprefix=tabprefix)
      

def yieldSTResidualsMC(opts, tabname, tabprefix):
    bffilename = 'bf_stat'
    bffile = tools.set_file(
        extbase=attr.brfpath, prefix=tabprefix, comname=bffilename)
    tab = DHadCBXTable()
    tab.column_append_from_dict('Mode', 'fname,fnamebar')     
    tab.column_append(parse_result(bffile, 'residual_single_mc'),
                      'Residual', rnd='1.')
    tab.column_append(parse_result(bffile, 'residual_chi2_single_mc'),
                      '$\chi^2$', rnd='0.1')
    tab.output(tabname, tabprefix=tabprefix)
      
   
