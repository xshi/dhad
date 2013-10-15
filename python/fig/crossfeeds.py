"""
Module for Cross Feed Study

"""

import os
import sys
import tools
import attr

from tools.filetools import UserFile
from attr.modes import modes
from tools import DHadTable
from fit.crossfeeds import get_single_modes, pair_to_str

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):

    dt_type = args[0]
    stage = args[1] 
    label = args[2]+'/crossfeeds'

    single_modes = get_single_modes(opts.set)
        
    org = UserFile()
    org.append(attr.fig_web_header)

    if stage == 'diag':
        for mode, sign in single_modes:
            msg = create_fig_diag_mode(dt_type, stage, label, mode, sign)
            org.append(msg)

    elif stage == 'nondiag':
        for x, y  in [(x, y) for x in single_modes for y in single_modes if x!=y]:
            sys.stdout.write('Creating mode %s, %s ... ' % (x, y))
            sys.stdout.flush()
            msg = create_fig_nondiag_mode(dt_type, stage, label, x, y)
            org.append(msg)
            sys.stdout.write('OK.\n')
    else:
        raise NameError(stage)

    figname = 'crossfeeds_' + '_'.join(args).replace('/', '_')
    
    org.append(attr.fig_web_footer)

    figlabel = label.split('/')[0]

    figname = figname.replace(figlabel, '')
    figname = figname.replace('__', '_')

    orgname = figname+'.org'
    orgname = orgname.replace('_.org', '.org')
    orgpath = os.path.join(attr.figpath, figlabel)
    orgfile = tools.check_and_join(orgpath, orgname)

    verbose = opts.verbose
    if opts.test:
        verbose = 1

    org.output(orgfile, verbose=verbose)
    orglink = '[[./fig/%s/%s][figure]]' %(figlabel, orgname)
    sys.stdout.write('\n%s\n\n' % orglink)

    if opts.test:
        return
    
    tools.org_export_as_html(orgfile)


    
def create_fig_diag_mode(dt_type, stage, label, mode, sign):

    prefix='dir_'+label

    if sign == 1:
        uname = modes[mode]['uname']
        fname = modes[mode]['fname']
        title = modes[mode]['orgname']
    else:
        uname = modes[mode]['unamebar']
        fname = modes[mode]['fnamebar']
        title = modes[mode]['orgnamebar']

    comname = '%s_Single_%s_fakes_Single_%s' % (dt_type, fname, fname)

    epsfile  = tools.set_file(extbase=attr.figpath,
                              prefix=prefix, comname=comname+'.eps')

    pdffile  = epsfile.replace('.eps', '.pdf')

    figlabel = label.split('/')[0]
    relpath = label.replace(figlabel, '')

    pdflink = '.%s/%s.pdf' %(relpath, comname)
    pnglink = '.%s/%s.png' %(relpath, comname)

    if not os.access(pdffile, os.F_OK):
        if not os.access(epsfile, os.F_OK):
            sys.stdout.write('epsfile is not ready for (%s %s) \n' % (mode, sign))
        else:
            tools.eps2png(epsfile)
            tools.eps2pdf(epsfile)


    figlink = '[[%s][%s]]' %(pdflink, pnglink)
    
    txtfile  = tools.set_file(extbase=attr.fitpath,
                              prefix=prefix, comname=comname+'.txt')


    logname = 'stage_%s_%s_%s.txt' %(stage, mode, sign)
    logfile = tools.set_file(extbase=attr.logpath,
                              prefix=prefix, comname=logname)
    loglink = ''
    if os.access(logfile, os.F_OK):
        loglink = '[[../../log/%s/%s][log]]' %(label, logname)

    tablink = ''
    if os.access(txtfile, os.F_OK):
        orgtabfile = txtfile.replace('.txt', '.org')
        tab = DHadTable(txtfile)
        tab.output_org(orgtabfile)

        abspath = os.path.join(attr.base)#, attr.analysis)
        orgtabfile = orgtabfile.replace(abspath, '../..')

        tablink = '#+INCLUDE: "%s"\n' % orgtabfile

    msg = '\n* %s \n  %s \n\n%s\n %s\n' % (
        title, figlink, tablink, loglink)

    return msg

def create_fig_nondiag_mode(dt_type, stage, label, x, y):
    prefix='dir_'+label
    if x[1] == 1:
        uname = modes[x[0]]['uname']
        fname = modes[x[0]]['fname']
        title1 = modes[x[0]]['orgname']
    else:
        uname = modes[x[0]]['unamebar']
        fname = modes[x[0]]['fnamebar']
        title1 = modes[x[0]]['orgnamebar']

    if y[1] == 1:
        unameb = modes[y[0]]['uname']
        fnameb = modes[y[0]]['fname']
        title2 = modes[y[0]]['orgname']
    else:
        unameb = modes[y[0]]['unamebar']
        fnameb = modes[y[0]]['fnamebar']
        title2 = modes[y[0]]['orgnamebar']

    title = '%s fakes %s' % (title1, title2)

    comname = '%s_Single_%s_fakes_Single_%s' % (dt_type, fname, fnameb)

    epsfile  = tools.set_file(extbase=attr.figpath,
                              prefix=prefix, comname=comname+'.eps')

    pdffile  = epsfile.replace('.eps', '.pdf')
    
    figlabel = label.split('/')[0]
    relpath = label.replace(figlabel, '')
    pdflink = '.%s/%s.pdf' %(relpath, comname)
    pnglink = '.%s/%s.png' %(relpath, comname)

    if not os.access(pdffile, os.F_OK):
        if not os.access(epsfile, os.F_OK):
            sys.stdout.write('epsfile is not ready for %s, %s \n' % (x, y))
        else:
            sys.stdout.write('Converting %s ...' % epsfile)
            tools.eps2png(epsfile)
            tools.eps2pdf(epsfile)
            sys.stdout.write(' OK.\n')
        
    figlink = '[[%s][%s]]' %(pdflink, pnglink)
    
    txtfile  = tools.set_file(extbase=attr.fitpath,
                              prefix=prefix, comname=comname+'.txt')
    xstr = pair_to_str(x)
    ystr = pair_to_str(y)
    
    logname = 'stage_%s_%s_%s.txt' %(stage, xstr,ystr)
    logfile = tools.set_file(extbase=attr.logpath,
                              prefix=prefix, comname=logname)
    if not os.access(epsfile, os.F_OK):
        sys.stdout.write('Please check log: %s\n' % logfile)

    loglink = ''
    if os.access(logfile, os.F_OK):
        loglink = '[[../../log/%s/%s][log]]' %(label, logname)
    tablink = ''

    if os.access(txtfile, os.F_OK):
        orgtabfile = txtfile.replace('.txt', '.org')
        tab = DHadTable(txtfile)
        tab.output_org(orgtabfile)

        abspath = os.path.join(attr.base)#, attr.analysis)
        orgtabfile = orgtabfile.replace(abspath, '../..')

        tablink = '#+INCLUDE: "%s"\n' % orgtabfile

    msg = '\n* %s \n  %s \n\n%s\n %s\n' % (
        title, figlink, tablink, loglink)

    return msg
