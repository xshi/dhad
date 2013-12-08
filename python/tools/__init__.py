"""
Tools for the D-Hadronic analysis scripts. 

"""
from __future__ import division

import os 
import sys
import re
import subprocess
import distutils.version
import difflib
import time
import shutil
import filecmp
import types
import math
import ROOT
import shelve
import attr
from uncertainties import ufloat

from tabletools import UserTable
from ttree import PyTTree
from ttree import DecayTreeNode
from attr.pdg import *
from attr.modes import dmode_revdict, dmode_dict
from filetools import UserFile
from attr import get_dataset_by_run, get_generated_numbers
from cuts import remove_gamma



__author__ = "Xin Shi <xs32@cornell.edu>"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2006-2011 Xin Shi"
__license__ = "GNU GPL"



def main(opts, args):
    
    if args[0] == 'ln':
	ln(args[1:])
    else:
	raise NameError(args)


class DHadTable(UserTable):
    '''Class to handle the table file  '''

    def __init__(self, filename=None, evalcell=False):
        UserTable.__init__(self, filename, evalcell=evalcell)

    def column_append_from_dict(self, title, key, opt=None, mode=None):
        if mode == None:
            mode_keys = attr.modes.keys()
        else:
            if isinstance(mode, str):
                mode_keys = map(int, mode.split(','))
            else:
                mode_keys = []
                mode_keys.append(mode)
                
        modes = attr.modes
            
        keyList = key.split(',')
        key = keyList[0]
        if len(keyList) > 1:
            keybar = keyList[1]
            
        aList = []
        aList.append(title)

        if opt == None:
            for m in mode_keys:
                for k in keyList:
                    name = str(modes[m][k])
                    if 'hname' in key:
                        name = '<literal>' + name + '</literal>'
                    aList.append(name)

        elif opt == 'double':
            for i, j in  attr.PossibleDoubleTags:
                name = modes[i][key] + ' ' + modes[j][keybar]
                if key == 'hname':
                    name = '<literal>' + name + '</literal>'
                aList.append(name)

        elif opt == 'double-dz':
            for i, j in  attr.DoubleTags_DZ:
                name = modes[i][key] + ' ' + modes[j][keybar]
                if key == 'hname':
                    name = '<literal>' + name + '</literal>'
                aList.append(name)

        elif opt == 'double-dp':
            for i, j in  attr.DoubleTags_DP:
                name = modes[i][key] + ' ' + modes[j][keybar]
                if key == 'hname':
                    name = '<literal>' + name + '</literal>'
                aList.append(name)

        self.column_append(aList)
        

    def column_append_from_fit_files(self, title, args, para, tag, rnd=None):

        parsed_args = parse_tab_args(args)
        rowName = para
        extbase = parsed_args['fitbase']
        prefix = parsed_args['prefix']
        dt_type = parsed_args['dt_type']
        ext = 'txt'
        self.column_append_from_files(title, rowName, extbase, prefix, 
                                      dt_type, tag, ext, rnd=rnd)
        
                        
    def column_append_from_files(self, title, rowName, extbase, prefix, 
                                 dt_type, tag, ext, 
                                 rnd=None, factor=None, err_type=None, 
                                 colName='Value,Error',
                                 sign = None, 
                                 mode=None, debug=False):
        aList = []
        aList.append(title)
        fileList = set_file_list(extbase, prefix, dt_type, 
                                 tag, ext, sign, mode=mode)

        if debug:
            sys.stdout.write('\ndebug: %s\n' %fileList)
        self.column_append_from_file_list(title, fileList, rowName, 
                                          colName, rnd, factor, err_type)



        
    def column_append_from_tab_file(self, title, tabfile, headname = None,
                                    rnd=None, factor=None, row = None, mode=None):
        
        
        if headname == None:
            headname = title

        tempTable = UserTable(tabfile) 

        if mode == None:
            aList = tempTable.column_get(headname)
            aList[0] = title

        else:
            mode = int(mode)
            aList = []
            aList.append(title)
            names = ['fname', 'fnamebar']
            col_ = headname
            for name in names:
                row_ = attr.modes[mode][name]
                cell = tempTable.cell_get(row_, col_)
                aList.append(cell)
            
        if row:
            start = row.split(':')[0]
            end   = row.split(':')[1]
            if start and end:
                start = int(start)
                end   = int(end)
                aList = aList[start:end]
            if start and not end:
                start = int(start)
                aList = aList[start:]
                aList.insert(0, title)
            if end and not start:
                end   = int(end)
                aList = aList[:end]
                
        self.column_append(aList)     
        if rnd or factor:
            self.column_trim(title, rnd, factor)
        return aList
    

    def diff_sigma_pct(self, tabB):
        tab_ = DHadTable()
        other = UserTable.diff_sigma_pct(self, tabB)
        tab_.input_tab(other)
        return tab_
        
    def output(self, tab_name=None, tabbase=attr.tabpath,
               orgheader=attr.tab_web_header,
               orgfooter = attr.tab_web_footer,
               trans_dict = None,
               verbose=0, test=False, export_html=True,
               label=None):

        if tab_name == None:
            self.output_txt()
            return

        if label != None:
            tablabel = label.split('/')[0]
            tabprefix = '_'.join(label.split('/')[1:])
            tabbase = os.path.join(tabbase, tablabel)
            if tabprefix != '':
                tab_name = '%s_%s' % (tabprefix, tab_name)
                                     

        txtfile  = set_file('txt', extbase=tabbase, comname=tab_name)
        if test:
            self.output_txt()
            sys.stdout.write('\ntest: txtfile %s\n' %txtfile)
            return

        self.output_txt(txtfile)

        infofile = set_file('info', extbase=tabbase, comname=tab_name)
        if not os.access(infofile, os.F_OK) :
            open(infofile, "a") 

        infopath, infoname = os.path.split(infofile)
        infoheader = '#+INCLUDE: "./%s"\n' % infoname
        orgheader += infoheader

        orgfile = set_file('org', extbase=tabbase, comname=tab_name)
        if self.cell_get(0, 0) == 'Mode':
            sample_cell = self.cell_get(1, 0)
            if ' ' in sample_cell:
                org_dict = attr.double_org_dict
            else:
                org_dict = attr.single_org_dict
            self.column_replace_by_translation('Mode', org_dict)
        elif self.cell_get(0, 0) == 'Modes':
            org_dict = attr.general_org_dict 
            self.column_replace_by_translate_elements('Modes', org_dict)

        if trans_dict:
            self.column_replace_by_translation(0, trans_dict)

        self.output_org(orgfile, orgheader, orgfooter, verbose=verbose)

        if export_html:
            infolink = '[[./tab/%s.info][info]]' % tab_name
            orglink = '[[./tab/%s.org][table]]' % tab_name
            if label != None:
                infolink = '[[./tab/%s/%s.info][info]]' % (tablabel, tab_name)
                orglink = '[[./tab/%s/%s.org][table]]' % (tablabel, tab_name)
                
            sys.stdout.write(' => %s (%s)\n' % (orglink, infolink))
            org_export_as_html(orgfile)


class DHadCBXTable(DHadTable):
    '''Class to handle the CBX table file  '''

    def __init__(self, filename=None):
        DHadTable.__init__(self, filename)

    def output(self, tabname=None, texhead=None,
               tabbase=attr.cbxtabpath, trans_dict=None,
               texstyle=None, outputtxt=False, tabprefix=None):

        if tabprefix != None:
            if 'dir_' in tabprefix:
                tabdir = tabprefix.replace('dir_', '')
                tabbase = os.path.join(tabbase, tabdir)

        if outputtxt:
            txtfile = set_file('txt', extbase=tabbase, comname=tabname)
            self.output_txt(txtfile)
        else:   
            self.output_txt()
            
        if tabname == None:
            return

        if self.cell_get(0, 0) == 'Mode':
            sample_cell = self.cell_get(1, 0)
            if ' ' in sample_cell:
                tex_dict = attr.double_tex_dict
            else:
                tex_dict = attr.single_tex_dict
            self.column_replace_by_translation('Mode', tex_dict)

        if trans_dict:
            self.column_replace_by_translation(0, trans_dict)

        texfile = set_file('tex', extbase=tabbase, comname=tabname)
        self.output_tex(texfile, texhead=texhead, texstyle=texstyle)

        
class THSTable(DHadCBXTable):
    '''Class to handle the Thesis table file  '''

    def __init__(self, filename=None):
        DHadTable.__init__(self, filename)


class PRDTable(DHadCBXTable):
    '''Class to handle the PRD table file  '''

    def __init__(self, filename=None):
        DHadTable.__init__(self, filename)


class EventsFile(UserFile):
    "handle events file"

    def __init__(self, filename=None):
        UserFile.__init__(self, filename)
        self.events = {}
        self.runs = {}
        self.datasets = {}
        self.datasets_sorted = []
        self.parse()
        
    def parse(self):
        line_no = 0
        for line in self.data:
            line_no += 1
	    elems = line.strip().split(' ')
            elems = [li for li in elems if li]
	    event = {}
	    run_no = int(elems[0])
            evt_no = int(elems[1])
            dataset = get_dataset_by_run(run_no)
	    event['run'] = run_no
            event['event'] = evt_no
            event['dataset'] = dataset
	    self.events[line_no] = event

            if run_no not in self.runs.keys():
                self.runs[run_no] = 1
            else:
                self.runs[run_no] += 1

            if dataset not in self.datasets.keys():
                self.datasets[dataset] = 1
            else:
                self.datasets[dataset] += 1

        dt_sorted = []

        for dataset in attr.datasets_281:
            if dataset in self.datasets.keys():
                dt_sorted.append(self.datasets[dataset])
            else:
                dt_sorted.append(0)
            
        self.datasets_sorted = dt_sorted
            
class ptobj(object):
    def __init__(self, pte, index):
        self.pte = pte
        self.index = index

    def __getattr__(self, name):
        return self.pte.__getattr__(name)[self.index]

    def __eq__(self, other):
        return isinstance(other, ptobj) and self.__cmp__(other) == 0

    def __ne__(self, other):
        return not isinstance(other, ptobj) or self.__cmp__(other) != 0

    def __cmp__(self, other):
        return self.index - other.index

    def as_obj(self, name):
        return ptobj(self.pte, self.__getattr__(name))


# ----------------------------------------------------------
# Functions
# ----------------------------------------------------------
def add_rootfile(rootfile, obj='dnt', debug=False):
    pt = ROOT.TChain(obj)
    num = 0
    if isinstance(rootfile, str):
        num = pt.Add(rootfile)
    if isinstance(rootfile, list):
        for rf in rootfile:
            num += pt.Add(rf)
    if debug:
        sys.stdout.write('\ndebug: %s root file(s) added:\n%s\n'
                         % (num, rootfile))
    if num < 1:
        raise NameError('No rootfile added!', rootfile)

    pt = PyTTree(pt)
    return pt

def backup_output(outfile):
    bakfile = None
    if os.access(outfile, os.F_OK) :
        bakfile =  outfile+'.bak'
        shutil.copy2(outfile, bakfile)
    fo = open(outfile, 'w')
    return fo, bakfile


def backup_and_remove(logfile):
    if os.access(logfile, os.F_OK):
        bakfile = logfile+'.bak'
        sys.stdout.write('Backing up %s ...' % bakfile)
        shutil.copy2(logfile, bakfile)
        sys.stdout.write(' done.\n')
        sys.stdout.write('Removing %s ...' %logfile)
        os.remove(logfile)
        sys.stdout.write(' done.\n')

def calc_asy_syst(label, mode):
    tabfile = os.path.join(attr.cbxtabpath, label, 'CPAsymmetrySystematics.txt')
    t = DHadTable(tabfile)

    daus = attr.modes[mode]['daughter_defs'].values()
    kp = daus.count('K+')
    km = daus.count('K-')
    pip = daus.count('pi+')
    pim = daus.count('pi-')

    k_pair = min(kp, km)
    k_num = abs(kp - km) + k_pair 

    pi_pair = min(pip, pim)
    pi_num = abs(pip - pim) + pi_pair 

    k_trk = float(t.cell_get('K tracking', 'Systematic (%)'))
    k_pid = float(t.cell_get('K PID', 'Systematic (%)'))
    pi_trk = float(t.cell_get('$\pi$ tracking', 'Systematic (%)'))
    pi_pid = float(t.cell_get('$\pi$ PID', 'Systematic (%)'))

    if mode == 0:
        k_pid = 0.5
        
    syst = math.sqrt(k_num * (k_trk**2 + k_pid**2) + 
                     pi_num * (pi_trk**2 + pi_pid**2))*.01

    return syst


def canvas_output(canvas, figname, label, test=False,
                  outputroot=True, outputhtml=True):

    figlabel = label.split('/')[0]
    relpath = label.replace(figlabel, '')

    figname = figname.replace(figlabel, '')
    if figname[-1] == '_':
        figname = figname[:-1]

    if test:
        figname += '.test'

    epsfile = os.path.join(attr.figpath, label, figname+'.eps')
    if test:
        sys.stdout.write('Will save as %s \n' % epsfile)

    canvas.SaveAs(epsfile)
    if outputroot:
        rootfile = os.path.join(attr.figpath, label, figname+'.root')
        canvas.SaveAs(rootfile)
        
    eps2png(epsfile)
    eps2pdf(epsfile)

    if test or not outputhtml:
        return
    
    org = UserFile()
    org.append(attr.fig_web_header)

    pdflink = '.%s/%s.pdf' %(relpath, figname)
    pnglink = '.%s/%s.png' %(relpath, figname)
    figlink = '[[%s][%s]]\n' %(pdflink, pnglink)

    org.append(figlink)
    org.append(attr.fig_web_footer)
    orgname = '%s.org' % figname
    orgfile = os.path.join(attr.figpath, label, orgname)
    org.output(orgfile)

    orglink = '[[./fig/%s/%s][figure]]' %(label, orgname)
    sys.stdout.write('\n%s\n\n' % orglink)
    org_export_as_html(orgfile)
    

def check_and_copy(source_file, dest_file, verbose=0):
    message = ''
    local_source_file = None
    if '@' in source_file and ':' in source_file:
        local_source_file = dest_file+'.remote'
        try:
            p = subprocess.Popen(['scp', source_file, local_source_file])
            os.waitpid(p.pid, 0)
            source_file = local_source_file
        except IOError:
            sys.stdout.write('Skipping %s \n' %source_file)
            return 

    if os.access(dest_file, os.F_OK) :
        if filecmp.cmp(source_file, dest_file, shallow=False):
            message =  'up-to-date: %s' % dest_file
        else:
            message = 'Updating %s ...' %dest_file
    else:
        message = 'Writing %s ...' %dest_file
    try:
        shutil.copy2(source_file, dest_file)
    except IOError:
        sys.stdout.write('Skipping %s \n' %source_file)
        return 
            
    if local_source_file != None:
        os.remove(local_source_file)

    if verbose > 0:
        sys.stdout.write(message+'\n')
        
    return message


def check_and_join(filepath, filename):
    if not os.access(filepath, os.F_OK):
        sys.stdout.write('Creating dir %s ...' % filepath)
        os.makedirs(filepath)
        sys.stdout.write(' OK.\n')

    return os.path.join(filepath, filename)


def check_output(fo, outfile, bakfile):
    fo.close()

    if bakfile == None:
        message = 'creating %s ...' %outfile
    
    else:
        if not filecmp.cmp(outfile, bakfile, shallow=False):
            message = 'updating %s ... ' % outfile
        else:
            os.remove(bakfile)
            message = 'up-to-date: %s' % outfile
    
    sys.stdout.write(message+'\n')

def combine_files(a, b, c, verbose=None):
    fa = open(a,'r')
    if verbose:
        print 'a', a
        print 'b', b
        print 'Generating combined evt file... '

    fc = open(c,'w')
    for line in fa:
        fc.write(line)
        
    if a == b:
        sys.stdout.write('Two identical files, use only one. \n')
    else:
        fb = open(b,'r')
        for line in fb:
            fc.write(line)
        fb.close()
        
    fa.close()
    fc.close()

    if verbose:
        print 'Generate complete.\n ', c

def combine_files_list(files, c):
    fc = open(c,'w')
    for f in files:
        fa = open(f,'r')
        for line in fa:
            fc.write(line)
        fa.close()

    fc.close()


def cosangle(p4a, p4b=(0,0,0,1)):
    len1 = pmag(p4a)
    len2 = pmag(p4b)
    return dot(p4a,p4b)/(len1*len2)


def count_lines(filename):
    count = 0
    for line in open(filename):
        count = count + 1
    return count

def count_mcdmodes(modedict, mcdmode, mcdbmode):
    mcdmode = remove_gamma(mcdmode)
    mcdbmode = remove_gamma(mcdbmode)
    modepair = '%s,%s' %(mcdmode, mcdbmode)

    if modepair in modedict:
        modedict[modepair] += 1
    else:
        modedict[modepair] =1

    return modedict


def create_bash_file_pyline(opts, label, dt_type, pyline,
                            bashname, optcommand='', subdir=''):
    script_dir =  os.path.join(attr.datpath, dt_type, label, 'src', subdir)

    bash_content =  '''#!/bin/sh
#$ -S /usr/local/bin/bash
#$ -j y
#$ -m a
#$ -M xs32@cornell.edu

date
hostname

.  ~/.bashrc
setdhad %s 

%s

python -c '%s'

date

''' % (attr.version, optcommand, pyline)
    
    bash_file = os.path.join(script_dir, bashname)

    verbose = opts.verbose
    if opts.test:
        verbose = 1
    f = UserFile()
    f.append(bash_content) 
    f.output(bash_file, verbose=verbose)
    os.chmod(bash_file, 0755)
    return bash_file


def data_bkg_double(opts, prefix):
    brfilename = 'bf_stat_sys'
    brfile = set_file(extbase=attr.brfpath, prefix=prefix,
                      comname=brfilename)
    bkg_list = get_column_from_file(
        brfile,
        start_line_str   = 'Fb',
        start_column_str = '',
        end_column_str   = '(',
        end_line_str     = 'Eff-corrected, bkg-subt yields',
        verbose          =  opts.verbose)
    double_bkg_list = bkg_list[18:]
    return double_bkg_list


def data_bkg_single(opts, prefix):
    brfilename = 'bf_stat_sys'
    brfile = set_file(extbase=attr.brfpath, prefix=prefix,
                      comname=brfilename)
    bkg_list = get_column_from_file(
        brfile,
        start_line_str   = 'Fb',
        start_column_str = '',
        end_column_str   = '(',
        end_line_str     = 'Eff-corrected, bkg-subt yields',
        verbose          = opts.verbose)
    single_bkg_list = bkg_list[:18]
    return single_bkg_list


def diff(fa, fb):
    sizea = os.path.getsize(fa)
    sizeb = os.path.getsize(fb)
    delta = sizeb - sizea
    return delta


def dot(p4a, p4b):
    return (p4a[1]*p4b[1]+p4a[2]*p4b[2]+p4a[3]*p4b[3])


def draw_hist(hists, xtitle, ytitle, legend=None, reverse=False):
    canvas = ROOT.TCanvas('canvas', 'canvas', 600, 630)

    if not isinstance(hists, list):
        hists = [hists]
    
    hist_list = [ (hist, hist.GetMaximum()) for hist in hists ] 

    hist_list.sort()
    if reverse:
        hist_list.reverse()
        
    i = 0
    for hist, val in hist_list:
        i += 1
        if i == 1:
            hist.SetLineWidth(3)
            hist.SetLineColor(i)
            hist.GetXaxis().SetTitle(xtitle)
            hist.GetYaxis().SetTitle(ytitle)
            hist.Draw()
        else:
            hist.SetLineWidth(3)
            hist.SetLineColor(i)
            hist.Draw("same")

        if legend != None:
            legend.AddEntry(hist, hist.GetName())

    if legend != None:
        legend.SetFillColor(0)
        legend.SetBorderSize(1)
        legend.Draw()
        
    return canvas


def duration_human(seconds):
    seconds = long(round(seconds))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365.242199)
 
    minutes = long(minutes)
    hours = long(hours)
    days = long(days)
    years = long(years)
 
    duration = []
    if years > 0:
        duration.append('%d year' % years + 's'*(years != 1))
    else:
        if days > 0:
            duration.append('%d day' % days + 's'*(days != 1))
        if hours > 0:
            duration.append('%d hour' % hours + 's'*(hours != 1))
        if minutes > 0:
            duration.append('%d minute' % minutes + 's'*(minutes != 1))
        if seconds > 0:
            duration.append('%d second' % seconds + 's'*(seconds != 1))
    return ' '.join(duration)


def eps2pdf(epsfile):
    args = ['epstopdf %s' % epsfile]
    process = subprocess.Popen(args, shell=True)
    output = process.communicate()[0]
    if output:
        raise NameError(output)


def eps2png(epsfile):
    args = ['eps2png %s' % epsfile]
    process = subprocess.Popen(args, shell=True)
    output = process.communicate()[0]
    if output:
        raise NameError(output)


def fill_hist_evtfile(hist, evtfile):
    sys.stdout.write('Filling %s ...' % evtfile)
    fo = open(evtfile, 'r')
    num = 0 
    for line in fo:
        num += 1
        hist.Fill(float(line))
    fo.close()
    sys.stdout.write(' %s done.\n' % num)
    return hist
    

def flatten(L):
    if not isinstance(L,list): return [L]
    if L == []: return L
    return flatten(L[0]) + flatten(L[1:])

    
def fourvecadd(*p4s):
    return map(sum, zip(*p4s)[:4])


def getfnamestr(pair):
    if pair[1] == 1:
        return modes[pair[0]]['fname']
    else:
        return modes[pair[0]]['fnamebar']

def get_cleandoulbe_name(fname):
    modekey, sign = get_modekey_sign(fname)
    if modekey in [0, 1, 3]:
        vsmode = 0
    else:
        vsmode = 200
    if sign == 1:
        pmode = modekey
        mmode = vsmode
    else:
        pmode = vsmode
        mmode = modekey

    doublename = 'Double_%s__%s' % (attr.modes[pmode]['fname'],
                                    attr.modes[mmode]['fnamebar'])
    return doublename


def get_column_from_file(filename,
                         start_line_str=None,
                         start_column_str = None,
                         end_column_str=None,
                         end_line_str =None,
                         skip_line_num = 0,
                         verbose = 0):

    part_file = get_part_file(filename, start_line_str, end_line_str,
                              skip_line_num=skip_line_num)
    column = []
    for line in part_file:
        if end_column_str not in line:
            continue
            
        tmp_part = line
        if start_column_str and isinstance(start_column_str, list):
            for sct in start_column_str:
                if sct not in line :
                    continue
                tmp_part = tmp_part.split(sct)[1]
                    
        if start_column_str and isinstance(start_column_str, str):
            if start_column_str not in line:
                continue
            tmp_part = tmp_part.split(start_column_str)[1]

        cell =  tmp_part.split(end_column_str)[0].strip()

        if cell:
            column.append(cell)

    if verbose > 0:
        print '\n'.join(column)
    return column


def get_corrected_abs_bkg(Matrix, Yld):
    # Do covariance for 2x2 matrix inversion a la hep-ex/9909031

    # mat = [[.454, 1],
    #        [.0072, 1]]
    # sigmat = [[.002, .1],
    #           [.0003, .1]]

    mat = Matrix[0]
    sigmat = Matrix[1]
    
    det = mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
    
    matinv = [[mat[1][1]/det, -mat[0][1]/det],
              [-mat[1][0]/det, mat[0][0]/det]]
    
    cov = {}
    rng = [(0,0), (0,1), (1,0), (1,1)]
    for a, b in [(x, y) for x in rng for y in rng]:
        tv = 0
        for i in xrange(2):
            for j in xrange(2):
                tv += (matinv[a[0]][i]*matinv[b[0]][i]
                       *sigmat[i][j]**2
                       *matinv[j][a[1]]*matinv[j][b[1]])
        cov[(a,b)] = tv
        
    # Y = [5809.,
    #      171.5]
    # Yerr = [56.9, 13.8]
    
    Y = Yld[0]
    Yerr = Yld[1]
    
    N = [0,
         0]

    for i in xrange(2):
        for j in xrange(2):
            N[i] += (matinv[i][j])*(Y[j])

    Ncovstat = {}
    Ncovsyst = {}
    for i in xrange(2):
        for j in xrange(2):
            Ncovstat[(i,j)] = 0
            Ncovsyst[(i,j)] = 0
            for k in xrange(2):
                for l in xrange(2):
                    Ncovsyst[(i,j)] += Y[k]*Y[l]*cov[((i,k),(j,l))]
            for k in xrange(2):
                Ncovstat[(i,j)] += matinv[i][k]*matinv[j][k]*Yerr[k]**2

##    for i in xrange(2):
##        print i, N[i], '+-', Ncovstat[(i,i)]**.5, '+-', Ncovsyst[(i,i)]**.5

    absbkg = '%s +/- %s +/- %s' % (N[1], Ncovstat[(1,1)]**.5,
                                   Ncovsyst[(1,1)]**.5)
    #print mode, Ncovstat
    return absbkg 


def get_eff_matrix_sideband(mode, label, bkg_sb_factor=1):
    sigfile = os.path.join(attr.cbxtabpath, label, 'singletag_sigmc_eff.txt')
    t = DHadTable(sigfile)
    modename = attr.modes[mode]['fname']
    sigeff = t.cell_get(modename, 'Efficiency(%)')
    sigeff = t.cell_times(sigeff, 0.01)

    sbfile = os.path.join(attr.cbxtabpath, label, 'kssidebandeff.txt')
    t = DHadTable(sbfile)
    sbeff = t.cell_get(modename, 'Eff')
    sbeff = t.cell_times(sbeff, 0.001)
    
    sigeff_val = float(sigeff.split('+/-')[0])
    sigeff_err = float(sigeff.split('+/-')[1])
    
    sbeff_val = float(sbeff.split('+/-')[0])
    sbeff_err = float(sbeff.split('+/-')[1])

    bkg_sbeff_val = bkg_sb_factor
    bkg_sbeff_err = 0.1

    bkg_sigeff_val = 1
    bkg_sigeff_err = 0.1
    
    Matrix = [ [[sigeff_val, bkg_sigeff_val], [sbeff_val, bkg_sbeff_val]],
               [[sigeff_err, bkg_sigeff_err], [sbeff_err, bkg_sbeff_err]] ]
   
    return Matrix

    
    
def get_evt_file(extbase, typename, tagname, fname, prefix=''):
    if prefix == '':
        evt_file  = os.path.join(
            extbase, typename+'_'+tagname+'_'+fname+'.evt')

    elif '/cleandouble' in prefix:
        extbase = extbase.replace('/cleandouble', '')
        cleandoublename = get_cleandoulbe_name(tagname+'_'+fname)
        evt_file  = os.path.join(
            extbase, typename+'_'+cleandoublename+'.evt')
    else:
        evt_file  = os.path.join(
            extbase, prefix+typename+'_'+tagname+'_'+fname+'.evt')

    return evt_file


def get_files_with_commonname(filepath, comname, suffix, exclude=None):
    filenames = []
    for root, dirs, files in os.walk(filepath):
	for name in files:
            if exclude != None and exclude in name:
                continue
            if comname in name and name.split('.')[-1] == suffix:
                filenames.append(name)
                
    return sorted(filenames)


def get_fname(pair):
    if pair[1] == 1:
        return attr.modes[pair[0]]['fname']
    else:
        return attr.modes[pair[0]]['fnamebar']


def get_generic_mctruth(mode, label):
    var = 'mctruth'
    datatype = 'generic'
    tag = 'Single'
    modename = attr.modes[mode]['fname']
    bkgname = attr.modes[mode]['bkg_multipions']

    evtname = '%s_%s_%s.evt' %(datatype, tag, modename)
    evtfile = os.path.join(attr.datpath, 'evt', label, 'var', var, evtname)

    if bkgname == 'Dp_to_pipipi':
        bkg_dmode = mcstringtodmode('pi+ pi- pi+')
    elif bkgname == 'Dp_to_pipipipi0':
        bkg_dmode = mcstringtodmode('pi+ pi- pi+ pi0')
    elif bkgname == 'Dp_to_pipipipipi':
        bkg_dmode = mcstringtodmode('pi+ pi- pi+ pi- pi+')
    else:
        raise NameError(bkgname)
    
    f = open(evtfile, 'r')
    count = 0 
    for line in f:
        mcdmodes = line.split('|')[0]
        if 'Mode' in mcdmodes:
            continue
        mcdmode = int(mcdmodes.split(',')[0])
        mcdmode = mcDmodeFixRad(mcdmode)
        if bkg_dmode == mcdmode:
            number = line.split('|')[1]
            count += int(number)
    f.close()
    return count


def get_modekey(modename):
    if modename.startswith('Single_') :
        modename = modename.replace('Single_', '')
        modename = modename.split('__')[0]

        for k, v in attr.modes.items():
            if v['fname'] == modename or v['fnamebar'] == modename \
                   or v['cname'] == modename:
                modekey = k 
                break

    elif modename.startswith('Double_') :
        modenames = modename.replace('Double_', '').split('__')
        for k, v in attr.modes.items():
            if v['fname'] == modenames[0] :
                modekey0 = k
            if v['fnamebar'] == modenames[1] :
                modekey1 = k
        modekey = (modekey0, modekey1)
    
    else:
        raise NameError(modename)

    return modekey


def get_modekey_sign(modename):
    if modename.startswith('Single_') :
        modename = modename.replace('Single_', '')
        modename = modename.split('__')[0]

        for k, v in attr.modes.items():
            if v['fname'] == modename :
                modekey = k
                sign = 1
            if v['fnamebar'] == modename:
                modekey = k
                sign = -1
            if v['cname'] == modename:
                modekey = k
                sign = [-1, 1] 
                
    elif modename.startswith('Double_') :
        modenames = modename.replace('Double_', '').split('__')

        for k, v in attr.modes.items():
            if v['fname'] == modenames[0] :
                modekey0 = k
            if v['fnamebar'] == modenames[1] :
                modekey1 = k
            
        modekey = (modekey0, modekey1)
        sign = None

    else:
        raise NameError(modename)
    
    return modekey, sign


def get_mode_root_name(mode):
    modekey, sign = get_modekey_sign(mode)
    if sign == 1:
        rootname = attr.modes[modekey]['uname']
    else:
        rootname = attr.modes[modekey]['unamebar']
    return rootname
    


def get_multspec_reweight(reweight, datatype, mode, label):
    from ROOT import TFile

    selname = '%s_%s.root' %(datatype, mode)
    selpath = os.path.join(attr.datpath, 'sel', label, 'multspec', reweight)
    selfile = check_and_join(selpath, selname)

    efffile = selfile.replace('.root', '.db')
    effs = shelve.open(efffile)

    npi0_denoms =  effs['npi0_denom'] 
    ntr_denoms = effs['ntr_denom']

    unweight_sum = effs['unweight_sum']
    reweight_ntr_sum  = effs['reweight_ntr_sum']
    reweight_npi0_sum = effs['reweight_npi0_sum']
    f = TFile(selfile)
    # gen_dmbc_ntr = {}; gen_dmbc_npi0 = {}
    # for i in range(7+1):
    #     gen_dmbc_ntr[i] = f.Get('gen_dmbc_ntr_'+`i`)
    # for i in range(5+1):
    #     gen_dmbc_npi0[i] = f.Get('gen_dmbc_npi0_'+`i`)
        
    # for i in gen_dmbc_ntr:
    #     if gen_dmbc_ntr[i].Integral() != 0:
    #         print 'efficiency for %d tracks' % i,\
    #               gen_dmbc_ntr[i].Integral()/ntr_denoms[i]

    # for i in gen_dmbc_npi0:
    #     if gen_dmbc_npi0[i].Integral() != 0:
    #         print 'efficiency for %d pi0' % i, \
    #               gen_dmbc_npi0[i].Integral()/npi0_denoms[i]
            
    # for i in ntr_denoms:
    #     print i, 'tracks:', ntr_denoms[i]/float(unweight_sum)
    # for i in npi0_denoms:
    #     print i, 'pi0:', npi0_denoms[i]/float(unweight_sum)

    unweight_dmbc = f.Get('unweight_dmbc')
    reweight_ntr_dmbc = f.Get('reweight_ntr_dmbc')
    reweight_npi0_dmbc = f.Get('reweight_npi0_dmbc')

    uwt = unweight_dmbc.Integral()/unweight_sum
    trk_rwt = reweight_ntr_dmbc.Integral()/reweight_ntr_sum
    pi0_rwt = reweight_npi0_dmbc.Integral()/reweight_npi0_sum

    # print 'Unweight', uwt
    # print 'Track reweight', trk_rwt
    # print 'Pi0 reweight', pi0_rwt
    
    trk_diff = uwt - trk_rwt
    pi0_diff = uwt - pi0_rwt

    return trk_diff, pi0_diff 

def get_orgname_from_fname(modename):
    modekey, sign = get_modekey_sign(modename)

    if sign == 1:
        orgname = attr.modes[modekey]['orgname']
    else:
        orgname = attr.modes[modekey]['orgnamebar']
    return orgname

def get_part_file(filename, start_line_str, end_line_str,
                  skip_line_num = 0, verbose = 0):

    fo = open(filename, 'r')
    part_file = []
    is_inside = False
    other_parts = None
    if isinstance(start_line_str, list):
        other_parts = start_line_str[1:]
        start_line_str = start_line_str[0]

    for line in fo:
        if start_line_str in line:
            is_inside = True
            part_file = []
        if end_line_str in line:
            is_inside = False

        if is_inside:
            if skip_line_num == 0:
                part_file.append(line)
            else:
                skip_line_num -= 1

    fo.close()

    if other_parts != None:
        for part in other_parts:
            for line in part_file:
                if part in line:
                    new_start = part_file.index(line)
                    part_file = part_file[new_start:]
                    break

    return part_file


def get_rootfile(datatype, mode=None, label=None, opt='', test=False):
    datpath = attr.datpath
    if datatype == 'signal':
        rootname = mode + '.root'
        if 'And' in mode:
            ddbar = mode.split('_')[1]
            d = ddbar.split('And')[0]
            dbar = ddbar.split('And')[1]
            rootname1 = rootname.replace(ddbar, d)
            rootname2 = rootname.replace(ddbar, dbar)
            rootname = [rootname1, rootname2]

    elif datatype in ['data', 'generic', 'generic/cont']:
        rootname = '*.root'
        if test and datatype == 'generic':
            rootname = '*data43_10_4_1.root'
    else:
        raise NameError(datatype)

    if datatype == 'generic':
        datatype = datatype+'/ddbar'

    if '/widede' in label or '/nofsr' in label or '/trig' in label or \
           '/desideband' in label or '281ipbv7/srs' in label:
        label = label.split('/')[0]

    dtuple_dir = ''
    if datatype == 'signal':
        if '281ipbv12' in label or '537ipbv12' in label or \
               '818ipbv12' in label :
            dtuple_dir = 'dtuple_'+attr.cleog+'_'+attr.pass2

    rootfile = os.path.join(datpath, datatype, label, dtuple_dir, rootname)

    if '818ipb' in label:
        rootfile = []
        label_281 = label.replace('818ipb', '281ipb')
        label_537 = label.replace('818ipb', '537ipb')
        
        if isinstance(rootname, str):
            rootfile_281 = os.path.join(datpath, datatype, label_281,
                                        dtuple_dir, rootname)
            rootfile_537 = os.path.join(datpath, datatype, label_537,
                                        dtuple_dir, rootname)
            rootfile = [rootfile_281, rootfile_537]
        if isinstance(rootname, list):
            for rn in rootname:
                rootfile_281 = os.path.join(datpath, datatype, label_281,
                                            dtuple_dir,  rn)
                rootfile_537 = os.path.join(datpath, datatype, label_537,
                                            dtuple_dir,  rn)
                rootfile.append(rootfile_281)
                rootfile.append(rootfile_537)
    else:    
        rootfile = os.path.join(datpath, datatype, label, dtuple_dir, rootname)

    if opt == 'Create':
        touch_file(rootfile)
        
    return rootfile

    
def get_table_from_file(filename,
                        start_line_str=None,
                        end_line_str =None,
                        verbose = 0):

    table = []
    fo = open(filename, 'r')
    start = False
    
    for line in fo:
        line = line.strip()
        if not line: continue

        if type(start_line_str) == types.StringType:
            if start_line_str in line:
                start = True
                continue
            
        if type(start_line_str) == types.ListType:

            if len(start_line_str) == 1:
                start_line_str  = start_line_str[0]
                continue

            if start_line_str[0] in line:
                del start_line_str[0]
                continue

        if end_line_str in line:
            start = False
            break

        if  start :
            table.append(line)

    fo.close()
    return table


def get_yld_vector_sideband(datatype, mode, label):
    prefix='dir_%s' % label
    sigfile = set_file('txt', datatype, mode, 'single',
                       prefix=prefix, extbase=attr.fitpath)

    t = DHadTable(sigfile)
    sigyld_val = float(t.cell_get('N1', 'Value'))
    sigyld_err = float(t.cell_get('N1', 'Error'))
    
    sbprefix='dir_%s/kssideband' % label
    if datatype == 'data' and mode in (202, 203):
        sbprefix += '/fix_sigmap1'
    sbfile = set_file('txt', datatype, mode, 'single',
                      prefix=sbprefix, extbase=attr.fitpath)

    t = DHadTable(sbfile)
    sbyld_val = float(t.cell_get('N1', 'Value'))
    sbyld_err = float(t.cell_get('N1', 'Error'))
 
    Vector = [ [sigyld_val, sbyld_val],
               [sigyld_err, sbyld_err] ]
   
    return Vector


def invmass(*p4s):
    return math.sqrt(invmasssq(*p4s))


def invmasssq(*p4s):
    etamunu = (1, -1, -1, -1)
    total = map(sum, zip(*p4s))
##    sum = fourvecadd(p4a, p4b)
    return sum(map(lambda x: x[0]*x[0]*x[1], zip(total, etamunu)))


def ln(args):
    src_dir = os.path.join(attr.base, args[0])
    dst_dir = os.path.join(attr.base, args[1])
    linked = 0
    skipped = 0 
    for root, dirs, files in os.walk(src_dir):
	for name in files:
	    src_file = os.path.join(src_dir, name)
	    dst_file = os.path.join(dst_dir, name)
	    try:
		os.symlink(src_file, dst_file)
		linked += 1
	    except OSError:
		sys.stdout.write('Skipping %s ...\n' %name)
		skipped += 1

	sys.stdout.write('Linked  ....... %s\n' %linked)
	sys.stdout.write('Skipped ....... %s\n' %skipped)
	sys.stdout.write('Total   ....... %s\n' %(linked+skipped))


def ln_files(srcdir, dstdir, pattern=None):
    if not os.path.exists(dstdir):
        os.mkdir(dstdir)

    fs = []
    for root, dirs, files in os.walk(srcdir):
        fs.extend(files)
        break
    
    if pattern is None:
        src_fs = fs
    else:
        src_fs = [f for f in fs if pattern in f]
        
    n_lnk = 0 
    cwd = os.getcwd()
    os.chdir(dstdir)
    for f in src_fs:
        src = os.path.join(srcdir, f)
        try:
            os.symlink(src, f)
            n_lnk += 1

        except OSError:
            pass 

    os.chdir(cwd)
    sys.stdout.write('Linked %s files. \n' %n_lnk)



def makeDDecaySubTree(pte, sign):
    top = None
    nodes = []
    for i in range(pte.nmcpart):
        if sign*pte.mcpdgid[i] in (pdgid_Dz, pdgid_Dp, pdgid_Dsp):
            top = i
            nodes.append(DecayTreeNode())
            nodes[0].setIndex(top)
            nodes[0].setPdgId(pte.mcpdgid[top])
            break
    if top != None:
        refs = { top: 0 }
        for i in range(top, pte.nmcpart):
            if pte.mcparent[i] in refs:
                index = len(nodes)
                refs[i] = index
                nodes.append(DecayTreeNode())
                nodes[index].setIndex(i)
                nodes[index].setPdgId(pte.mcpdgid[i])
                if pte.mcparent[i] >= 0:
                    parent = nodes[refs[pte.mcparent[i]]]
                    nodes[index].addParent(parent)
                    parent.addDaughter(nodes[index])
    return nodes


def makeDecayTree(pte):
    nodes = []
    for i in range(pte.nmcpart):
        nodes.append(DecayTreeNode())
        nodes[i].setIndex(i)
        nodes[i].setPdgId(pte.mcpdgid[i])
        if pte.mcparent[i] >= 0:
            parent = nodes[pte.mcparent[i]]
            nodes[i].addParent(parent)
            parent.addDaughter(nodes[i])
    return nodes


def matrix_inv_cov_epsilon(mode, label):
    # Do covariance for 2x2 matrix inversion a la hep-ex/9909031
    # define convenience for summing in quadrature
    def quadsum(input1, input2):
        return (input1[0]+input2[0], (input1[1]**2+input2[1]**2)**.5)

    def quadsub(input1, input2):
        return (input1[0]-input2[0], (input1[1]**2+input2[1]**2)**.5)
    
    def getF(n, m):
        val = n[0]/(n[0]+m[0])
        error = 1/(n[0]+m[0])*((val*m[1])**2+((1-val)*n[1])**2)**.5
        return (val, error)

    def get_yld(dt_type, mode, tag, prefix):
        fitpath = attr.fitpath
        txtfile = set_file('txt', dt_type, mode, tag,
                           prefix=prefix, extbase=fitpath)
        tab = DHadTable(txtfile)
        yld1 = (float(tab.cell_get('N1', 'Value')),
                float(tab.cell_get('N1', 'Error')))
        yld2 = (float(tab.cell_get('N2', 'Value')),
                float(tab.cell_get('N2', 'Error')))
        return quadsum(yld1, yld2)
        
    mul_yld_signal = get_yld('signal', mode, 'single',
                              'dir_%s/multiple_candidate' % label)  
    sing_yld_signal = get_yld('signal', mode, 'single',
                               'dir_%s/single_candidate' % label)  
    mul_yld_generic = get_yld('generic', mode, 'single',
                              'dir_%s/multiple_candidate' % label)  
    sing_yld_generic = get_yld('generic', mode, 'single',
                               'dir_%s/single_candidate' % label)  
    
    sum_yld_generic = quadsum(mul_yld_generic, sing_yld_generic)

    sum_yld_signal = quadsum(mul_yld_signal, sing_yld_signal)

    mul_yld_dt = get_yld('signal', mode, 'single',
                         'dir_%s/multiple_candidate/cleandouble' % label)
    sing_yld_dt = get_yld('signal', mode, 'single',
                          'dir_%s/single_candidate/cleandouble' % label)
    sum_yld_dt = quadsum(mul_yld_dt, sing_yld_dt)
    f1 = getF(mul_yld_generic, sing_yld_generic)
    f2 = getF(mul_yld_dt, sing_yld_dt)
    mul_yld_data = get_yld('data', mode, 'single',
                           'dir_%s/multiple_candidate' % label)

    sing_yld_data = get_yld('data', mode, 'single',
                            'dir_%s/single_candidate' % label)
    fdata = getF(mul_yld_data, sing_yld_data)
    N1 = sum(get_generated_numbers('single', mode=mode))
    N2 = sum(get_generated_numbers('double', mode=mode))

    mat = [[1-f1[0], f1[0]],
           [1-f2[0], f2[0]]]
    sigmat = [[f1[1], f1[1]],
              [f2[1], f2[1]]]
    
    det = mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
    #print 'Determinant is', det
    matinv = [[mat[1][1]/det, -mat[0][1]/det],
          [-mat[1][0]/det, mat[0][0]/det]]

    cov = {}
    rng = [(0,0), (0,1), (1,0), (1,1)]
    
    for a, b in [(x, y) for x in rng for y in rng]:
        tv = 0
        for i in xrange(2):
            for j in xrange(2):
                tv += (matinv[a[0]][i]*matinv[b[0]][i]
                       *sigmat[i][j]**2
                       *matinv[j][a[1]]*matinv[j][b[1]])
        cov[(a,b)] = tv

    # print matinv
    # print '----------'
    # for i in cov:
    #     print i, cov[i]
    # print '----------'

    # E = [N1/sum_yld_generic[0],
    #      N2/sum_yld_dt[0]]
    #         # not binomial but eh
    # Eerr = [N1/sum_yld_generic[0]**2*sum_yld_generic[1],
    #         N2/sum_yld_dt[0]**2*sum_yld_dt[1]]
    E = [N1/sum_yld_signal[0],
         N2/sum_yld_dt[0]]
            # not binomial but eh
    Eerr = [N1/sum_yld_signal[0]**2*sum_yld_signal[1],
            N2/sum_yld_dt[0]**2*sum_yld_dt[1]]
    
    N = [0,
         0]

    for i in xrange(2):
        for j in xrange(2):
            N[i] += (matinv[i][j])*(E[j])

    # print N
    # print '----------'
    Ncovstat = {}
    Ncovsyst = {}
    for i in xrange(2):
        for j in xrange(2):
            Ncovstat[(i,j)] = 0
            Ncovsyst[(i,j)] = 0
            for k in xrange(2):
                for l in xrange(2):
                    Ncovsyst[(i,j)] += E[k]*E[l]*cov[((i,k),(j,l))]
            for k in xrange(2):
                Ncovstat[(i,j)] += matinv[i][k]*matinv[j][k]*Eerr[k]**2
    # print Ncovstat
    # print Ncovsyst
    
    # print '---------- In short:'
    # for i in xrange(2):
    #     print i, N[i], '+-', Ncovstat[(i,i)]**.5, '+-', Ncovsyst[(i,i)]**.5

    # print '--------------local information'
    # print 'epsilon_s:', 1/N[0], '+-', 1/N[0]**2*(Ncovstat[(0,0)]+Ncovsyst[(0,0)])**.5
    # print 'epsilon_MC:', 1/E[0], '+-', 1/E[0]**2*Eerr[0]
    # print 'F_dt: %s +- %s' % f2
    # print 'F_mc: %s +- %s' % f1
    # print 'F_data: %s +- %s' % fdata
    # print 'F_mc-F_data: %s +- %s' % quadsub(f1, fdata)
    zeta = (fdata[0]/f1[0]-1)*(E[0]/N[0]-1)
    dzetadfdata = 1/f1[0]*(E[0]/N[0]-1)
    dzetadfmc = (fdata[0]/f1[0]**2)*(E[0]/N[0]-1)
    dzetades = (fdata[0]/f1[0]-1)*E[0]
    dzetademc = (fdata[0]/f1[0]-1)*(E[0]**2/N[0])
    
    dzeta = ((dzetadfdata*fdata[1])**2+
             (dzetadfmc*f1[1])**2+
             (dzetades**2*1/N[0]**4*(Ncovstat[(0,0)]+Ncovsyst[(0,0)]))+
             (dzetademc*1/E[0]**2*Eerr[0])**2)**.5
    #print 'zeta: %s +- %s' % (zeta, dzeta)

    F_data = '%s +/- %s' % fdata
    F_MC = '%s +/- %s' % f1
    F_Diff = '%s +/- %s' %  quadsub(f1, fdata)
    Delta = '%s +/- %s' % (zeta, dzeta)
    
    return F_data, F_MC, F_Diff, Delta

    
def mcDmodeFixRad(mcdmode):
    rp1 = 10000000
    rp2 = 1000000
    return mcdmode - ((mcdmode % rp1) - (mcdmode % rp2))


def mcdmodetostring(mcdmode):
    str = `mcdmode`
    retstrs = []
    for i in range(len(str)-1, -1, -1):
        for j in range(int(str[i])):
            retstrs.append(dmode_dict[10**(len(str)-1-i)] + ' ')
    return ''.join(retstrs)


def mcstringtodmode(mcstring):
    retval = 0
    import string
    l = string.split(mcstring, " ")
    for i in l:
        if i == "eta" or i == "eta'":
            i = "eta(')"
        if i not in dmode_revdict:
            print 'Error: no code for', i
            return retval
        retval += dmode_revdict[i]
    return retval


def merge_hist_files(result, histfiles):
    hadd = os.path.join(os.environ['ROOTSYS'], 'bin', 'hadd')
    cmd = '%s %s %s' %(hadd, result, ' '.join(histfiles))
    process_cmd(cmd)
                                                                    

def normalizedRooFitIntegral(function, integrationVar, lowerLimit, upperLimit):
    from ROOT import RooArgSet
    integral = function.createIntegral(RooArgSet(integrationVar))
    return (RooFitIntegral(function, integrationVar, lowerLimit, upperLimit)/
            integral.getVal())


def numbers_to_string(numbers):

    strnums = map(str, numbers)

    string = ','.join(strnums)

    return string


def org_export_as_html(orgfile, verbose=0):
    loadfile = attr.orgsetup
    cmd = 'emacs -q --batch --load=%s --visit=%s --funcall\
    org-export-as-html-batch' %(loadfile, orgfile)

    sys.stdout.write('Exporting %s to html...' % orgfile)
    sys.stdout.flush()

    process_cmd(cmd, verbose=verbose)


def output_modedict(modedict, modefile):
    f = UserFile()
    f.data.append('Mode || Number \n')
    for k, v in modedict.items():
        f.data.append('%s | %s \n' %(k, v))
    f.output(modefile)


def pair_to_str(x):
    if x[1] == 1:
        signx = 'p'
    else:
        signx = 'm'
    string = '%s%s' %(x[0], signx)
    return string


def parse_args(args):
    if args[0] not in ['signal', 'data', 'generic',
                       'generic/cont', 'generic/ddbar',
                       'generic/radret', 'generic/tau',
                       'signal/data', 'generic/data',
                       'signal,data']:
	raise NameError(args)

    datatype = args[0] 

    tag = 'single'
    if args[1].startswith('Single'):
        modes = [args[1]]

    elif args[1] == 'single':
        modes = attr.single_mode_list

    elif args[1] == 'single_p':
        modes = attr.single_mode_list_p
        
    elif args[1] == 'single_m':
        modes = attr.single_mode_list_m

    elif args[1] == 'diagsingle':
        modes = attr.diag_single_mode_list

    elif args[1] == 'diagsingle_ks':
        modes = attr.diag_single_mode_list_ks

    elif args[1] == 'single_ks':
        modes = attr.single_mode_list_ks

    elif args[1] == 'single_ks_p':
        modes = attr.single_mode_list_ks_p

    elif args[1].startswith('Double'):
        modes = [args[1]]
        tag = 'double'
        
    elif args[1] == 'diagdouble':
        modes = attr.diag_double_mode_list
        tag = 'double'
        
    elif args[1] == 'nondiagdouble':
        modes = attr.nondiag_double_mode_list
        tag = 'double'

    elif args[1] == 'cleandouble':
        modes = attr.clean_double_mode_list
        tag = 'double'
        
    elif args[1] == 'double':
        modes = attr.double_mode_list
        tag = 'double'

    elif args[1] == 'double_all_d0s':
        modes = ['double_all_d0s']
        tag = 'double'

    elif args[1] == 'double_all_dps':
        modes = ['double_all_dps']
        tag = 'double'

    elif args[1].startswith('single/'):
        except_mode = args[1].split('/')[1]
        modes = attr.single_mode_list
        modes.remove(except_mode)

    else:
        raise ValueError(args)

    label = args[2]

    parsed = []
    parsed.append(datatype)
    parsed.append(tag)
    parsed.append(modes)
    parsed.append(label)
    return parsed


def parse_evtname(opts, evt):

    label = evt
    ver = opts.analysis
    evtbase = attr.evtpath(ver)
    prefix =  'dir_'+ evt

    name_items = evt.split('/')
    ver_maybe = name_items[0]
    if len(name_items) > 1:
        label_maybe = evt.split('/')[1]

    if ver_maybe in attr.versions:
        ver = ver_maybe
        evtbase = attr.evtpath(ver)
        if label_maybe :
            prefix = 'dir_' + label_maybe
        else:
            raise NameError(evt)
        
    return label, evtbase, prefix

def parse_opts_set(set_, name_=''):
    value_ = None
    if set_ == None or '=' not in set_:
        return value_
    for li in set_.split(','):
        if '=' not in li:
            continue
        name = li.split('=')[0]
        value = li.split('=')[1]
        if name == name_:
            if '-' in value:
                value_ = value
            else:
                try:
                    value_ = eval(value)
                except NameError:
                    value_ = value
            sys.stdout.write('Set %s = %s \n' % (name, value)) 
    return value_


def parse_result(bffile, var, verbose = 0):

    if var == 'paras':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Fitted parameters',
            start_column_str = '',
            end_column_str   = '=',
            end_line_str     = 'Difference from seeds',
            verbose          = verbose)
        
    elif var == 'value_err':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Fitted parameters',
            start_column_str = '=',
            end_column_str   = '(',
            end_line_str     = 'Difference from seeds',
            verbose          = verbose)

    elif var == 'value':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Fitted parameters',
            start_column_str = '=',
            end_column_str   = '+-',
            end_line_str     = 'Difference from seeds',
            verbose          = verbose)

    elif var == 'err':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Fitted parameters',
            start_column_str = '+-',
            end_column_str   = '(',
            end_line_str     = 'Difference from seeds',
            verbose          = verbose)
    elif var == 'err_frac':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Fitted parameters',
            start_column_str = '(',
            end_column_str   = '%',
            end_line_str     = 'Difference from seeds',
            verbose          = verbose)

    elif var == 'stat':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Statistical and systematic errors',
            start_column_str = ':',
            end_column_str   = '(',
            end_line_str     = 'Residuals',
            verbose          = verbose)

    elif var == 'syst':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Statistical and systematic errors',
            start_column_str = 'stat',
            end_column_str   = '(',
            end_line_str     = 'Residuals',
            verbose          = verbose)

    elif var == 'stat_frac':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Statistical and systematic errors',
            start_column_str = '(',
            end_column_str   = '%',
            end_line_str     = 'Residuals',
            verbose          = verbose)

    elif var == 'syst_frac':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Statistical and systematic errors',
            start_column_str = ['stat', '('],
            end_column_str   = '%',
            end_line_str     = 'Residuals',
            verbose          = verbose)


    elif var == 'para_bf_ratio':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'D+2K-K+Pi+/D-2K+K-Pi-:',
            start_column_str = '',
            end_column_str   = '=',
            end_line_str     = 'sigma(D0D0bar)',
            skip_line_num    = 2, 
            verbose          = verbose)

    elif var == 'value_err_bf_ratio':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'D+2K-K+Pi+/D-2K+K-Pi-:',
            start_column_str = '=',
            end_column_str   = '(',
            end_line_str     = 'sigma(D0D0bar)',
            skip_line_num    = 2, 
            verbose          = verbose)

    elif var == 'value_bf_ratio':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'D+2K-K+Pi+/D-2K+K-Pi-:',
            start_column_str = '=',
            end_column_str   = '+-',
            end_line_str     = 'sigma(D0D0bar)',
            skip_line_num    = 2, 
            verbose          = verbose)

    elif var == 'stat_bf_ratio':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'D+2K-K+Pi+/D-2K+K-Pi-:',
            start_column_str = '+-',
            end_column_str   = '(',
            end_line_str     = 'sigma(D0D0bar)',
            skip_line_num    = 2, 
            verbose          = verbose)

    elif var == 'syst_bf_ratio':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'D+2K-K+Pi+/D-2K+K-Pi-:',
            start_column_str = '(stat) +-',
            end_column_str   = '(',
            end_line_str     = 'sigma(D0D0bar)',
            skip_line_num    = 2, 
            verbose          = verbose)

    elif var == 'corr_coef':
        var_list = get_table_from_file(
            bffile,
            start_line_str   = 'Correlation coefficients',
            end_line_str     = 'Global correlation coefficients',
            verbose          = verbose)

    elif var == 'global_corr':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = 'Global correlation coefficients',
            start_column_str = '',
            end_column_str   = '\n',
            end_line_str     = 'Enter statistical errors?',
            verbose          = verbose)

    elif var == 'residual_single':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Statistical and systematic errors',
                                'Residuals:'],
            start_column_str = ':',
            end_column_str   = ',',
            end_line_str     = 'D02K-Pi+/D0b2K+Pi-:',
            verbose          = verbose)

    elif var == 'residual_single_mc':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Enter statistical errors? (y/n):',
                                'Residuals:'],
            start_column_str = ':',
            end_column_str   = ',',
            end_line_str     = 'D02K-Pi+/D0b2K+Pi-:',
            verbose          = verbose)

    elif var == 'residual_chi2_single_mc':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Enter statistical errors? (y/n):',
                                'Residuals:'],
            start_column_str = '=',
            end_column_str   = '\n',
            end_line_str     = 'D02K-Pi+/D0b2K+Pi-:',
            verbose          = verbose)

    elif var == 'residual_double':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Statistical and systematic errors',
                                'Residuals:', 'D-2K+K-Pi-:'],
            start_column_str = ':',
            end_column_str   = ',',
            end_line_str     = 'BrD2KPiPi0 / BrD2KPi',
            verbose          = verbose)

    elif var == 'residual_double_dz':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Statistical and systematic errors',
                                'Residuals:', 'D-2K+K-Pi-:'],
            start_column_str = ':',
            end_column_str   = ',',
            end_line_str     = 'D+2K-Pi+Pi+/D-2K+Pi-Pi-:',
            verbose          = verbose)

    elif var == 'residual_double_dp':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Statistical and systematic errors',
                                'Residuals:',
                                'D+2K-Pi+Pi+/D-2K+Pi-Pi-:'],
            start_column_str = ':',
            end_column_str   = ',',
            end_line_str     = 'BrD2KPiPi0 / BrD2KPi',
            verbose          = verbose)

    elif var == 'residual_double_mc':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Enter statistical errors? (y/n):',
                                'Residuals:', 'D02K-Pi+/D0b2K+Pi-:'],
            start_column_str = ':',
            end_column_str   = ',',
            end_line_str     = 'BrD2KPiPi0 / BrD2KPi',
            verbose          = verbose)

    elif var == 'residual_chi2_double_mc':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Enter statistical errors? (y/n):',
                                'Residuals:', 'D02K-Pi+/D0b2K+Pi-:'],
            start_column_str = '=',
            end_column_str   = '\n',
            end_line_str     = 'BrD2KPiPi0 / BrD2KPi',
            verbose          = verbose)

    elif var == 'paras+ratio':
        var_A = 'paras'
        var_B = 'para_bf_ratio'
        
        var_list = parse_result(bffile, var_A)
        var_list.extend(parse_result(bffile, var_B))
        
    elif var == 'value_err+ratio':
        var_A = 'value_err'
        var_B = 'value_err_bf_ratio'
        var_list = parse_result(bffile, var_A)
        var_list.extend(parse_result(bffile, var_B))

    elif var == 'value+ratio':
        var_A = 'value'
        var_B = 'value_bf_ratio'
        var_list = parse_result(bffile, var_A)
        var_list.extend(parse_result(bffile, var_B))
        
    elif var == 'syst+ratio':
        var_A = 'syst'
        var_B = 'syst_bf_ratio'
        var_list = parse_result(bffile, var_A)
        var_list.extend(parse_result(bffile, var_B))

    elif var == 'stat+ratio':
        var_A = 'stat'
        var_B = 'stat_bf_ratio'
        var_list = parse_result(bffile, var_A)
        var_list.extend(parse_result(bffile, var_B))

    elif var == 'corr_eff':
        var_list = get_column_from_file(
            bffile,
            start_line_str   = ['Corrected efficiencies'],
            start_column_str = '',
            end_column_str   = '\n',
            end_line_str     = 'NDD mode by mode:',
            verbose          = verbose)


    elif var == 'st_eff':
        var_A = 'corr_eff'
        var_list = parse_result(bffile, var_A)
        st_eff, dt_dz_eff , dt_dp_eff = parse_corr_eff(var_list)
        var_list = st_eff

    elif var == 'dt_dz_eff':
        var_A = 'corr_eff'
        var_list = parse_result(bffile, var_A)
        st_eff, dt_dz_eff , dt_dp_eff = parse_corr_eff(var_list)
        var_list = dt_dz_eff

    elif var == 'dt_dp_eff':
        var_A = 'corr_eff'
        var_list = parse_result(bffile, var_A)
        st_eff, dt_dz_eff , dt_dp_eff = parse_corr_eff(var_list)
        var_list = dt_dp_eff

    else:
        raise NameError(var)

    return var_list

    
def parse_tabname(opts, tab):
    label = tab
    ver = opts.analysis
    fitbase = attr.fitpath(ver)
    prefix =  'dir_'+ tab

    name_items = tab.split('/')
    ver_maybe = name_items[0]
    if len(name_items) > 1:
        label_maybe = tab.split('/')[1]

    if ver_maybe in attr.versions:
        ver = ver_maybe
        fitbase = attr.fitpath(ver)
        if label_maybe :
            prefix = 'dir_' + label_maybe
        else:
            raise NameError(tab)
        
    return label, fitbase, prefix


def parse_tab_args(args):
    
    parsed_args ={}

    ver_maybe = args.split('/')[0]
    if ver_maybe in attr.versions:
        parsed_args['version'] = ver_maybe
        parsed_args['fitbase'] = attr.fitpath(ver_maybe)

        label = args.split('/')[1]
        parsed_args['prefix'] = 'dir_' + label
        parsed_args['dt_type'] = args.split('/')[2]
    else:
        raise ValueError(args)
        
    return parsed_args



def pmag(p4a):
    return math.sqrt(pmagsq(p4a))

def pmagsq(p4a):
    return sum(map(lambda x: x*x, p4a[1:4]))

def ptmag(p4a):
    return math.sqrt(ptmagsq(p4a))

def ptmagsq(p4a):
    return sum(map(lambda x: x*x, p4a[1:3]))


def print_sep(char = '-', num = 50):
    sys.stdout.write(char*num + '\n')


def process_cmd(cmd, test=False, verbose=1):
    if test:
        sys.stdout.write(cmd+'\n')
        return 

    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    stdout = process.communicate()[0]

    if verbose == 0:
        sys.stdout.write(' done.\n')
        
    if verbose > 0:
        sys.stdout.write(stdout)


def qsub_cmd(command, test=False):
    logname = command.replace(' ', '_')+'.log'
    logname = logname.replace(',', '_')
    logpath = os.path.join(attr.logpath, 'qsub')
    logfile = check_and_join(logpath, logname)
    
    bashname = 'qsub.sh'
    bashpath = os.path.join(attr.base, 'src', attr.version, 'bash')
    bash_content =  '''#!/bin/sh
#$ -S /usr/local/bin/bash
#$ -j y
#$ -m a
#$ -M xs32@cornell.edu

date
hostname

.  ~/.bashrc
setdhad %s 

%s

date

''' % (attr.version, command)

    bashfile = check_and_join(bashpath, bashname)
    
    f = UserFile()
    f.append(bash_content) 
    f.output(bashfile)
    os.chmod(bashfile, 0755)

    #cmd = 'qsub -l arch=lx24-x86 -o %s %s ' %(logfile, bashfile)
    cmd = 'qsub -l arch=lx24-amd64 -o %s %s ' %(logfile, bashfile)

    process_cmd(cmd, test)
    

def qsub_jobs(logfile, qjobname, bash_file, test=True) :
    if os.access(logfile, os.F_OK) and not test:
        os.remove(logfile)

    #cmd = 'qsub -l arch=lx24-x86 -o %s -N %s %s ' %(
    #    logfile, qjobname, bash_file)
    cmd = 'qsub -l arch=lx24-amd64 -o %s -N %s %s ' %(
        logfile, qjobname, bash_file)

    process_cmd(cmd, test)


def remove_duplicates_from_list(alist):
    blist = []
    for a in alist:
        if a not in blist:
            blist.append(a)
    return blist 


def RooFitIntegral(function, integrationVar, lowerLimit, upperLimit):
    from ROOT import RooArgSet
    try:
        # new way
        integrationVar.setRange('loc_intrange', lowerLimit, upperLimit)
        integral = function.createIntegral(integrationVar, integrationVar,
                                           ROOT.RooFit.Range('loc_intrange'))
        return integral.getVal()
    except:
        integral = function.createIntegral(RooArgSet(integrationVar))
        
##     oldLowerLimit = integrationVar.getFitMin()
##     oldUpperLimit = integrationVar.getFitMax()
##     integrationVar.setFitRange(lowerLimit, upperLimit)
        oldLowerLimit = integrationVar.getMin()
        oldUpperLimit = integrationVar.getMax()
        integrationVar.setRange(lowerLimit, upperLimit)
        
        unnormalizedIntegralValue = integral.getVal()
##     integrationVar.setFitRange(oldLowerLimit, oldUpperLimit)
        integrationVar.setRange(oldLowerLimit, oldUpperLimit)
        return unnormalizedIntegralValue


def set_root_style(stat=0, grid=0, PadTopMargin=0.08,
                   PadLeftMargin=0.10):
    # must be used in the beginning
    ROOT.gROOT.SetBatch(1)
    ROOT.gROOT.Reset()

    ROOT.gStyle.SetOptTitle(1) 
    ROOT.gStyle.SetTitleFillColor(0) 
    ROOT.gStyle.SetTitleBorderSize(0)
    
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetCanvasColor(0)
    ROOT.gStyle.SetCanvasDefX(0)
    ROOT.gStyle.SetCanvasDefY(0)
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetFrameBorderSize(1)
    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetFrameFillStyle(0)
    ROOT.gStyle.SetFrameLineColor(1)
    ROOT.gStyle.SetFrameLineStyle(1)
    ROOT.gStyle.SetFrameLineWidth(1)

    ROOT.gStyle.SetPadTopMargin(PadTopMargin) 
    ROOT.gStyle.SetPadLeftMargin(PadLeftMargin) 
    ROOT.gStyle.SetPadRightMargin(0.05) 

    ROOT.gStyle.SetLabelSize(0.03, "XYZ") 
    ROOT.gStyle.SetTitleSize(0.04, "XYZ") 
    ROOT.gStyle.SetTitleOffset(1.2, "Y") 

    ROOT.gStyle.SetPadBorderMode(0) 
    ROOT.gStyle.SetPadColor(0) 
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetPadGridX(grid)
    ROOT.gStyle.SetPadGridY(grid)

    ROOT.gStyle.SetOptStat(stat)
    ROOT.gStyle.SetStatColor(0)
    ROOT.gStyle.SetStatBorderSize(1)

    #ROOT.gStyle.SetLegendBorderSize(0)
    #ROOT.gStyle.SetLegendFillColor(0)


def set_file(ext=None, dt_type=None, mode=None, tag=None,
             sign=None,          
             prefix='',          
             extbase=None,       
             forceCombine = None,
             comname=None,       
             subdir    = ''):

    if dt_type != None:
        typename = dt_type
        if len(dt_type) == 1:
            typename = attr.TypeNames[dt_type]

    if tag != None:
        tagname = tag.capitalize()
        if len(tag) == 1:
            tagname  = attr.TagNames[tag]
        
    if mode != None:
        if isinstance(mode, str):
            try:
                mode = int(mode)
            except ValueError:
                if mode == 'double_all_d0s':
                    pass
                elif mode == 'double_all_dps':
                    pass
                else:
                    mode, sign = get_modekey_sign(mode)

        modes    = attr.modes

        fname     = ''
        fnamebar  = ''

        if mode == 'double_all_d0s':
            corename = 'all_D0s'
        elif mode == 'double_all_dps':
            corename = 'all_Dps'
        else:
            if tag == 's' or tag == 'single':
                fname     = modes[mode]['fname']
                fnamebar  = modes[mode]['fnamebar']

            elif tag == 'd' or tag == 'double':
                fname     = modes[mode[0]]['fname']
                fnamebar  = modes[mode[1]]['fnamebar']

            if sign == 1:
                corename  = fname
            elif sign == -1:
                corename  = fnamebar
            else:
                corename  = fname+ '__' +fnamebar

        if 'AND' in prefix:
            prefix = prefix.replace('AND', '')
            corename  = fname.split('_')[0]+ 'And' +fnamebar

        comname = typename+'_'+tagname+'_'+corename

    else:
        if comname == None:
            comname = typename+'_'+tagname

    evtprefix = ''
    if '818ipb' in prefix:
        evtprefix = prefix
    
    if 'dir' in prefix :
        subdir = prefix.split('dir_')[1]#.split('_')[0]
        if ',' in subdir:
            subdir = subdir.split(',')[0]
        prefix = prefix.replace('dir_'+subdir, '')
        prefix = prefix.replace('__', '_')

    if prefix != '':
        prefix = re.sub('^_', '', prefix)
        prefix = re.sub('_$', '', prefix)

        comname = prefix+'_'+comname


    if extbase == None:
        if ext :
            extfile = comname + '.' + ext
        else:
            extfile = comname
        return extfile
            
    if subdir != '':
        extbase = os.path.join(extbase, subdir)

    if not os.access(extbase, os.F_OK):
        if 'xs32@lnx' in extbase:
            sys.stdout.write('Using the remote dir: %s \n' %extbase)
        else:
            sys.stdout.write('Creating dir: %s ...' % extbase)
            os.makedirs(extbase)
            sys.stdout.write(' OK.\n')

    if ext: 
        extfile = os.path.join(extbase, comname + '.' + ext)
    else:
        extfile = os.path.join(extbase, comname)

    if forceCombine == 1:
        if '/cleandouble' in evtprefix :
            prefix = evtprefix

        file_a = get_evt_file(extbase, typename,tagname,fname, prefix)
        file_b = get_evt_file(extbase, typename,tagname,fnamebar, prefix)

        if not os.access(file_a, os.F_OK) or not os.access(file_b, os.F_OK):
            if '818ipb' in evtprefix:
                file_a_281ipb = file_a.replace('818ipb', '281ipb')
                file_a_537ipb = file_a.replace('818ipb', '537ipb')
                combine_files(file_a_281ipb, file_a_537ipb, file_a)
                file_b_281ipb = file_b.replace('818ipb', '281ipb')
                file_b_537ipb = file_b.replace('818ipb', '537ipb')
                combine_files(file_b_281ipb, file_b_537ipb, file_b)
            else:
                raise ValueError(file_a)

        combine_files(file_a, file_b, extfile)

    elif forceCombine == 'all_d0s':
        files = []
        for m in attr.double_d0_mode_list:
            file_ = os.path.join(extbase, typename+'_' + m + '.evt')
            files.append(file_)

        combine_files_list(files, extfile)

    elif forceCombine == 'all_dps':
        files = []
        for m in attr.double_dp_mode_list:
            file_ = os.path.join(extbase, typename+'_' + m + '.evt')
            files.append(file_)

        combine_files_list(files, extfile)

    return extfile




def set_file_list(extbase, prefix, dt_type, tag, ext, sign=None, mode=None):

    fileList = []

    if tag =='s' or tag == 'single':
        if mode == None:
            modelist = attr.modes.keys()
        else:
            if isinstance(mode, str):
                modelist = map(int, mode.split(','))
            else:
                modelist = []
                modelist.append(mode)

    elif tag == 'd' or tag == 'double':
        modelist = attr.PossibleDoubleTags

        if ('diag' in prefix and 'nondiag' not in prefix) or (
            'resolution' in prefix):
            modelist = attr.DiagDoubleTags
        if 'nondiag' in prefix :
            modelist = attr.NonDiagDoubleTags
    else:
        raise ValueError(tag)
    
    for mode in modelist:
        if sign == None:
            extfile = set_file(ext, dt_type, mode, tag,
                               prefix=prefix, extbase=extbase)
            fileList.append(extfile)
        else:
            signList = map(int, sign.split(','))
            for s in signList:
                extfile = set_file(
                    ext, dt_type, mode, tag, s,
                    prefix=prefix, extbase=extbase)
                fileList.append(extfile)
                
    return fileList


def save_fit_result(pars, txtfile, err_type='SYMM', verbose=0):
    f = UserFile()
    if err_type == 'SYMM':
        f.append('Name\t|| Value\t|| Error\n')
        for par in pars:
            line = '%s\t| %s\t| %s\n' %(
                par.GetName(), par.getVal(), par.getError())
            f.append(line)

    elif err_type == 'ASYM':
        f.append('Name\t|| Value\t|| Error\t|| Low\t || High\n')
        for par in pars:
            line = '%s\t| %s\t| %s\t| %s\t| %s\n' %(
                par.GetName(), par.getVal(), par.getError(),
                par.getAsymErrorLo(), par.getAsymErrorHi())
            f.append(line)

    else:
        raise NameError(err_type)
    
    f.output(txtfile, verbose=verbose)


def str_to_ufloat(s):
    if '<' in s:
        val = 0
        err = 0
    else:
        val = float(s.split('+/-')[0])
        err = float(s.split('+/-')[1])
    
    ufl = ufloat((val, err))
    return ufl
    

def touch_file(f):
    filepath, tail = os.path.split(f)
    if not os.access(filepath, os.F_OK):
        sys.stdout.write('Creating dir %s ...' % filepath)
        os.makedirs(filepath)
        sys.stdout.write(' OK.\n')


def trkFourTuple(ptobj, assumption, bremrecover=True):
    """ assumption: 1 = pi, 2 = kaon, 3 = mu, 4 = electron
    need to do bremsstrahlung recovery """
    if (assumption == 1 or assumption=='pi'):
        return (ptobj.trpie,
                ptobj.trpipx,
                ptobj.trpipy,
                ptobj.trpipz)
    elif (assumption == 2 or assumption=='k'):
        return (ptobj.trke,
                ptobj.trkpx,
                ptobj.trkpy,
                ptobj.trkpz)
    elif ((assumption == 3 or assumption=='mu') or
          (assumption == 4 or assumption=='e')):
##         # bremsstrahlung recovery method 1: preserves mass
##         if (assumption == 3 or assumption=='mu'):
##             code = 'mu+'
##         else:
##             code = 'e+'
##         if bremrecover:
##             brem = ptobj.trbremsum
##         else:
##             brem = 0
##         mom = math.sqrt(sum(map(lambda x: x**2, (ptobj.trpipx,
##                                                  ptobj.trpipy,
##                                                  ptobj.trpipz))))
##         # bremsstrahlung recovery: add shower energy to momentum,
##         # get new energy
##         scaling = 1+brem/mom
##         mom += brem
##         return (math.sqrt(mom**2+particle_data[code].mass**2),
##                 ptobj.trpipx*scaling,
##                 ptobj.trpipy*scaling,
##                 ptobj.trpipz*scaling)
        # brem recovery method 2: just add the bloody four-vectors
        if (assumption == 3 or assumption=='mu'):
            masssqdiff = pimumasssqdiff
        else:
            masssqdiff = piemasssqdiff
        oldvect = (math.sqrt(sq(ptobj.trpie)-masssqdiff),
                   ptobj.trpipx,
                   ptobj.trpipy,
                   ptobj.trpipz)
        if not bremrecover:
            return oldvect
        bremvec = (ptobj.trbremsum,
                   ptobj.trbrempx,
                   ptobj.trbrempy,
                   ptobj.trbrempz)
        return fourvecadd(oldvect, bremvec)
    else:
        return trkFourTuple(ptobj, 'pi')


def valid_version(ver):
    src = distutils.version.StrictVersion(attr.version)
    ver = distutils.version.StrictVersion(ver)
    if src != ver:
        return False
    
    return True

