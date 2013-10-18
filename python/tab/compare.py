"""
Script to create comparison table

"""
import os
import sys
import filecmp

import attr
import tools
from tools import DHadTable
import compare
import yld
from tools.filetools import UserFile 
from sets import Set

__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010-2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    label = args[-1]
    tabname = '%s/compare_%s' %(label, '_'.join(args[:-1]))
    function = getattr(compare, args[0])
    return function(opts, tabname, args[1:])


def yields(opts, tabname, args):
    if args[0] not in ['signal', 'data'] :
	raise NameError(args)

    rnd='.01'
    err_type=None
    diff = 'pct'
    sign = 1 
    if opts.set:
        for li in opts.set.split(':'):
            name = li.split('=')[0]
            value = li.split('=')[1]
            sys.stdout.write('Set %s = %s \n' % (name, value))
            if name == 'diff':
                diff = value
            if name == 'err_type':
                err_type = value
            if name == 'sign':
                sign = value

    variable = 'yields'
    dt_type = args[0]
    tag = args[1]
    label_A = args[2]
    label_B = args[3]
    fitbase = attr.fitbase

    sys.stdout.write('dhad.tab : Compare %s between %s and %s:\n' %(
        variable, label_A, label_B ))

    tab = DHadTable()
    namestyle = 'fname,fnamebar'
    tab.column_append_from_dict('Mode', namestyle)     
    tab.column_append_from_files(label_A, 'N1,N2', fitbase, 'dir_%s' %label_A,
                                 dt_type, tag ,'txt', rnd='1.')
    tab.column_append_from_files(label_B, 'N1,N2', fitbase, 'dir_%s' %label_B,
                                 dt_type, tag ,'txt', rnd='1.')

    if sign == '0':
        tab.rows_join_by_average(rnd='1.')

    if diff == 'pct':
        tab.column_append_by_diff_pct(
            'diff(%)', label_B,label_A, rnd=rnd, err_type=err_type)
    elif diff == 'sigma_pct':
        tab.column_append_by_diff_sigma_pct('diff(%)', label_B,label_A, rnd=rnd)
    elif diff == 'sigma2_pct':
        tab.column_append_by_diff_sigma2_pct('diff(%)', label_B,label_A, rnd=rnd)
    elif diff == 'ratio':
        tab.column_append_by_divide(
            'ratio', label_B,label_A, rnd=rnd, err_type='Indp')
    else:
        raise NameError(diff)

    tab.output(tabname, test=opts.test)


def ratios(args):
    if 'signal' in args[0]:
        ratios_signal(args[1:])
    else:
	raise NameError(args)

def ratios_signal(args):
    if args[0] == '537ipb/281ipb' and args[1] == '537ipbv2/281ipb':
        tabfilename1 = 'compare_yields_signal_divide_537ipb_9.03_regular12.txt'
        title1 = args[0]
        headname1 = title1 

        tabfilename2 = 'compare_yields_signal_divide_537ipbv2_9.03_regular12.txt'
        title2 = args[1]
        headname2 = title2
        
    else:
	raise NameError(args)
    
    tabfile1 = os.path.join(attr.tabpath, tabfilename1)
    tabfile2 = os.path.join(attr.tabpath, tabfilename2)

    if opts.set and opts.set == 'info':
        print 'here'
        
    
    tab  = DHadTable()
    tab.column_append_from_tab_file('Mode', tabfile1, 'Mode')
    tab.column_append_from_tab_file(title1, tabfile1, headname1)
    tab.column_append_from_tab_file(title2, tabfile2, headname2)
    tab.column_append_by_diff_sigma_pct('diff(%)', title2, title1)
    tab.output(_tabname)
   
def evtfile(args):

    if args[0] not in ['signal', 'data'] :
	raise NameError(args)

    variable = 'yields'
    dt_type = args[0]
    tag = args[1]
    
    evt_A =  args[2]
    evt_B =  args[3]

    label_A, evtbase_A, prefix_A = tools.parse_evtname(opts, evt_A) 
    label_B, evtbase_B, prefix_B = tools.parse_evtname(opts, evt_B) 

    filelist_A = tools.set_file_list(evtbase_A, prefix_A, dt_type, tag, 'evt')
    filelist_B = tools.set_file_list(evtbase_B, prefix_B, dt_type, tag, 'evt')
    zipped = zip(filelist_A, filelist_B)

    for f in zipped:
        fa = f[0]
        fb = f[1]

        diff = tools.diff(fa, fb)
        print diff
    sys.exit()

    sys.stdout.write('dhad.tab : Compare %s between %s and %s:' %(
        variable, tab_A, tab_B ))
    
    tab = DHadTable()
    namestyle = 'fname,fnamebar'
    tab.column_append_from_dict('Mode', namestyle)     
    tab.column_append_from_files(label_A, 'N1,N2', fitbase_A, prefix_A,
                                 dt_type, tag ,'txt', rnd='1.')
    tab.column_append_from_files(label_B, 'N1,N2', fitbase_B, prefix_B,
                                 dt_type, tag ,'txt', rnd='1.')
    tab.column_append_by_diff_sigma_pct('diff(%)', label_B,label_A, rnd=rnd)
    
    tab.output(_tabname)

def para(args):
    
    if '_'.join(args) == 'momentum_resolution':
        para_momentum_resolution()
    if args[0] == 'argus_p':
        para_argus('p', args[1:])
    elif args[0] == 'argus_xi':
        para_argus('xi', args[1:])
    elif args[0] == 'md':
        para_md(args[1:])
    else:    
        raise NameError(args)

def para_argus(para, args):
    namestyle = 'fname'
    rnd = '0.01'
    tag = 's'

    rowName = para
    extbase = attr.fitbase
    ext = 'txt'

    dt_type = args[0]
    tab_A = args[1]
    tab_B = args[2]

    label_A = tab_A
    label_B = tab_B

    label = tools.parseopts_set(opts.set, 'label')
    if label:
        labels = label.split(',')
        label_A = labels[0]
        label_B = labels[1]
    tab = DHadTable()
    tab.column_append_from_dict('Mode', namestyle)
    tab.column_append_from_files(label_A, rowName, extbase, 'dir_'+tab_A, 
                                 dt_type, tag, ext, rnd=rnd)
    tab.column_append_from_files(label_B, rowName, extbase, 'dir_'+tab_B, 
                                 dt_type, tag, ext, rnd=rnd)
    tab.column_append_by_diff_pct('diff(%)', label_B, label_A, rnd=rnd)
    tab.output(_tabname)

 
def para_momentum_resolution():

    if tools.valid_version('10.1.5'):
        tabnameA = 'line_shape_paras'
        tabnameB = 'para_momentum_resolution'
    else:
        raise NameError(attr.src)

    tabfileA = tools.set_file(extbase=attr.tabpath,
                              comname=tabnameA, ext='txt')

    tabfileB = tools.set_file(extbase=attr.tabpath,
                              comname=tabnameB, ext='txt')

    tabA = DHadTable(tabfileA)
    tabB = DHadTable(tabfileB)

    tab = tabA.diff_sigma_pct(tabB)

    tab.output(_tabname)

def para_md(args):

    para = 'md'
    namestyle = 'fname'
    rnd = '0.0000001'
    tag = 's'

    tab_A = args[0]
    tab_B = args[1]

    latel_A = tab_A
    latel_B = tab_B

    label = tools.parseopts_set(opts.set, 'label')

    if label:
        labels = label.split(',')
        label_A = labels[0]
        label_B = labels[1]
       
    tab = DHadTable()
    tab.column_append_from_dict('Mode', namestyle)
    tab.column_append_from_fit_files(label_A, tab_A, para, tag, rnd)
    tab.column_append_from_fit_files(label_B, tab_B, para, tag, rnd)
    tab.column_append_by_diff('diff[MeV]', label_B,label_A, rnd=rnd, factor=1000)

    tab.output(_tabname)

    
def pdg2004(args):
    '''
    --------------------------------------------------------
        Results of the Data Fit Compare with PDG 2004
    --------------------------------------------------------
    '''

    label = args[0]
    
    verbose  = opts.verbose

    bffilename = 'bf_stat_sys'
        
    bffile = os.path.join(attr.brfpath, label, bffilename)

    tab = DHadTable()
    tab.column_append(tools.parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(tools.parse_result(bffile, 'value'), 'value')

    tab.column_append(tools.parse_result(bffile, 'stat'),  'stat')
    tab.column_append(tools.parse_result(bffile, 'syst'),  'syst')
    tab.columns_join3('Fitted Value', 'value', 'stat',  'syst')

    tab.column_trim('Fitted Value', row = ['ND0D0Bar', 'ND+D-'],
                    rnd = '.001', factor = 0.000001, opt = '(cell)x10E6')
    tab.column_trim('Fitted Value', rnd = '.0001',
                    except_row = ['ND0D0Bar', 'ND+D-'])

    tab.column_append(tools.parse_result(bffile, 'err_frac'),
                      'Frac. Err', rnd = '.1', opt = '(cell%)')
    tab.columns_join('Fitted Value','Fitted Value','Frac. Err', str=' ')

    tab.column_append(attr.PDG2004_NBF, 'PDG 2004')
    tab.column_append_by_diff_sigma('Difference', 'Fitted Value', 'PDG 2004')

    tab.output(_tabname)#, trans_dict = attr.NBF_dict)


def pdg2009(args):
    '''
    --------------------------------------------------------
        Results of the Data Fit Compare with PDG 2009
    --------------------------------------------------------
    '''

    label = args[0]
    
    verbose  = opts.verbose

    bffilename = 'bf_stat_sys'
        
    bffile = os.path.join(attr.brfpath, label, bffilename)

    tab = DHadTable()
    tab.column_append(tools.parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(tools.parse_result(bffile, 'value'), 'value')

    tab.column_append(tools.parse_result(bffile, 'stat'),  'stat')
    tab.column_append(tools.parse_result(bffile, 'syst'),  'syst')
    tab.columns_join3('Fitted Value', 'value', 'stat',  'syst')

    tab.column_trim('Fitted Value', row = ['ND0D0Bar', 'ND+D-'],
                    rnd = '.001', factor = 0.000001, opt = '(cell)x10E6')
    tab.column_trim('Fitted Value', rnd = '.0001',
                    except_row = ['ND0D0Bar', 'ND+D-'])

    tab.column_append(tools.parse_result(bffile, 'err_frac'),
                      'Frac. Err', rnd = '.1', opt = '(cell%)')
    tab.columns_join('Fitted Value','Fitted Value','Frac. Err', str=' ')

    tab.column_append(attr.PDG2009_NBF, 'PDG 2009')
    tab.column_append_by_diff_sigma('Difference', 'Fitted Value', 'PDG 2009')

    tab.output(_tabname)




def brf_data_results(opts, tabname, args):
    '''
    -----------------------------
        Results of the Data Fit 
    -----------------------------
    '''

    label_A = args[0]
    label_B = args[1]
    
    verbose  = opts.verbose

    bffilename = 'bf_stat_sys'
        
    labels = []
    labels.append(label_A)
    labels.append(label_B)

    tab = DHadTable()
    paras = False

    for label in labels:
        if '281ipb' in label:
            factor =  0.000001
        elif '537ipb' in label:
            factor =  0.000001*281/537
        elif '818ipb' in label:
            factor =  0.000001*281/818
        else:
            raise NameError(label)

        if '818ipb' in label_A and '818ipb' in label_B:
            factor = 0.000001
            
        bffile = os.path.join(attr.brfpath, label, bffilename)
        if not paras:
            tab.column_append(tools.parse_result(bffile, 'paras'),
                              'Parameters')
            paras = True
        tab.column_append(tools.parse_result(bffile, 'value'), 'value', rnd='.00001' )
        tab.column_append(tools.parse_result(bffile, 'stat'),  'stat')
        tab.column_append(tools.parse_result(bffile, 'syst'),  'syst')
        tab.columns_join3('Fitted Value', 'value', 'stat',  'syst')
        tab.column_trim('Fitted Value', row=['ND0D0Bar', 'ND+D-'],
                        rnd='.0001', factor=factor, opt='(cell)x1E6')
        tab.column_trim('Fitted Value', rnd='.00001',
                        except_row=['ND0D0Bar', 'ND+D-'])
        tab.column_append(tools.parse_result(bffile, 'err_frac'),
                          'Frac. Err', rnd='.1', opt='(cell%)')
        tab.columns_join(label, 'Fitted Value','Frac. Err', str=' ')
    tab.column_append_by_diff_sigma('Difference', label_B,label_A)
    tab.output(tabname, test=opts.test)

    
def diff(args):

    label= None
    if opts.set:
        for li in opts.set.split(':'):
            name = li.split('=')[0]
            value = li.split('=')[1]
            sys.stdout.write('Set %s = %s \n' % (name, value))
            if name == 'label':
                label = value

    if label:
        labels = label.split(',')
        label_A = labels[0]
        label_B = labels[1]

    tab_A = 'compare_%s.txt' % args[0]
    tab_B = 'compare_%s.txt' % args[1]

    tabfile_A = os.path.join(attr.tabpath, tab_A)
    tabfile_B = os.path.join(attr.tabpath, tab_B)

    tab = DHadTable()
    tab.column_append_from_tab_file('Mode', tabfile_A, 'Mode')
    tab.column_append_from_tab_file(label_A, tabfile_A, 'diff(%)')
    tab.column_append_from_tab_file(label_B, tabfile_B, 'diff(%)')
    tab.column_append_by_diff('diff', label_B,label_A)
       
    tab.output(_tabname)
    

def dirs(args):

    if args[0].startswith('/'):
        dira = args[0]
    else:
        dira = os.path.join(attr.base, args[0])

    if  args[1].startswith('/'):
        dirb = args[1]
    else:
        dirb = os.path.join(attr.base, args[1])

    d = filecmp.dircmp(dira, dirb)

    d.report()

    sys.stdout.write('There are %s different files. \n' % len(d.diff_files))

def files(args):

    if args[0].startswith('/'):
        dira = args[0]
    else:
        dira = os.path.join(attr.base, args[0])

    if  args[1].startswith('/'):
        dirb = args[1]
    else:
        dirb = os.path.join(attr.base, args[1])

    d = filecmp.dircmp(dira, dirb)

    sys.stdout.write('There are %s different files. \n' % len(d.diff_files))

    tab = DHadTable()
    tab.row_append(['FileName', 'A', 'B'])

    for f in d.diff_files:
        filea = os.path.join(dira, f)
        fileb = os.path.join(dirb, f)

        tab.row_append_from_files(f, [filea, fileb])

    tab.output_org()


def entries(args):
    dt_type = args[0]
    tag = args[1]
    label_A = args[2]
    label_B = args[3]

    evtpath = attr.evtpath
    rnd='.01'
    err_type=None
    label = None
    diff = 'pct'
    
    tab = DHadTable()
    tab.row_append(['Mode', label_A, label_B])
    tab.head = tab.data[0]
    for mode in attr.modes:
        for sign in [1, -1]:
            evtfile_A = tools.set_file('evt', dt_type, mode, tag, sign=sign,
                                       prefix='dir_'+label_A, extbase=evtpath)
            evtfile_B = tools.set_file('evt', dt_type, mode, tag, sign=sign,
                                       prefix='dir_'+label_B, extbase=evtpath)
            entries_A = tools.count_lines(evtfile_A)
            entries_B = tools.count_lines(evtfile_B)
            if sign == 1:
                modename = attr.modes[mode]['fname']
            else:
                modename = attr.modes[mode]['fnamebar']
            row = [modename, entries_A, entries_B]
            tab.row_append(map(str, row))

    tab.column_append_by_diff_pct('diff(%)', label_B,label_A, rnd=rnd, err_type=err_type)
    tab.output(_tabname)

def events(args):

    parsed = yld.parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label_A   = parsed[3]
    label_B  = args[3]

    datpath = attr.datpath
    tab = DHadTable()
    tab.row_append(['Mode', label_A, label_B, 'Common',
                    'Unique(%s)' %label_A, 'Unique(%s)' %label_B ])
    tab.head = tab.data[0]
    for mode in modes:
        modename = mode.replace('Single_', '')
        evtname = datatype + '_' + mode + '.evt'
        evtpath_A = os.path.join(datpath, 'evt', label_A, 'events')
        evtfile_A = os.path.join(evtpath_A, evtname)
        f_A = UserFile(evtfile_A)
        events_A = Set(f_A.data)
        evtpath_B = os.path.join(datpath, 'evt', label_B, 'events')
        evtfile_B = os.path.join(evtpath_B, evtname)
        f_B = UserFile(evtfile_B)
        events_B = Set(f_B.data)
        events_inter = events_A & events_B
        entries_A = len(events_A)
        entries_B = len(events_B)
        common = len(events_inter)
        unique_A = len(events_A - events_inter)
        unique_B = len(events_B - events_inter)
        row = [modename, entries_A, entries_B, common, unique_A, unique_B]
        tab.row_append(map(str, row))
    tab.output(_tabname)
