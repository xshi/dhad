"""
Creating figures for D-Hadronic analysis. 

"""
import os
import sys
import attr
import tools
import ROOT
from tools.filetools import UserFile
from tools import DHadTable, get_modekey, parse_args
from fit import load_roofit_lib


__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2006-2011 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    if args[0] == 'backgrounds':
        import backgrounds
        backgrounds.main(opts, args[1:])
        return

    if args[0] == 'brs':
        import brs
        brs.main(opts, args[1:])
        return

    if args[0] == 'compare':
        import compare
        compare.main(opts, args[1:])
        return

    if args[0] == 'cbx':
        import cbx
        cbx.main(opts, args[1:])
        return

    if args[0] == 'crossfeeds':
        import crossfeeds
        crossfeeds.main(opts, args[1:])
        return

    if args[0] == 'evt':
        import evt
        evt.main(opts, args[1:])
        return

    if args[0] == 'fun':
        import fun
        fun.main(opts, args[1:])
        return

    if args[0] == 'kkmass':
        import kkmass
        kkmass.main(opts, args[1:])
        return

    if args[0] == 'kpimass':
        import kpimass
        kpimass.main(opts, args[1:])
        return

    if args[0] == 'trim':
        import trim
        trim.main(opts, args[1:])
        return

    if args[0] == 'trkmtm':
        import trkmtm
        trkmtm.main(opts, args[1:])
        return

    if args[0] == 'trkmtm1':
        import trkmtm1
        trkmtm1.main(opts, args[1:])
        return

    if args[0] == 'trkmtm2':
        import trkmtm2
        trkmtm2.main(opts, args[1:])
        return

    if args[0] == 'var':
        import var
        var.main(opts, args[1:])
        return


    figname = '_'.join(args).replace('/', '_')

    parsed = parse_args(args)
    dt_type  = parsed[0]
    tag = parsed[1]
    modes = parsed[2]
    label = parsed[3]

    sqrt = False
    if opts.set and opts.set == 'sqrt':
        sqrt = True

    linr = False
    if opts.set and opts.set == 'linr':
        linr = True


    org = UserFile()
    org.append(attr.fig_web_header)

    for mode in modes:
        if mode == 'double_all_d0s' or mode == 'double_all_dps' :
            modekey = mode
        else:
            modekey = get_modekey(mode)
        if sqrt:
            sqrt_fig_mode(tag, dt_type, modekey, label)
        sys.stdout.write('Creating %s ...' % mode)
        sys.stdout.flush()
        msg = create_fig_mode(tag, dt_type, modekey, label)
        sys.stdout.write(' OK.\n')
        org.append(msg)

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



def create_fig_mode(tag, dt_type, mode, label):
    if tag == 'single':
        modename = attr.modes[mode]['orgname']
    else:
        if mode == 'double_all_d0s':
            modename = 'Double all D0s'
        elif mode == 'double_all_dps':
            modename = 'Double all Dps'
        else:
            mode1 = mode[0]
            mode2 = mode[1]
            modename = '%s, %s' % (attr.modes[mode1]['orgname'],
                                   attr.modes[mode2]['orgnamebar'])

    prefix = 'dir_' + label
    epsfile = tools.set_file('eps', dt_type, mode, tag,
                             prefix=prefix, extbase=attr.figpath)

    head, tail = os.path.split(epsfile)
    comname = tail.replace('.eps', '')
    figlabel = label.split('/')[0]
    relpath = label.replace(figlabel, '')
    
    pdflink = '.%s/%s.pdf' %(relpath, comname)
    pnglink = '.%s/%s.png' %(relpath, comname)
    loglink = '[[../../log/%s/%s.txt][log]]' %(label, comname)
    figlink = '[[%s][%s]]' %(pdflink, pnglink)
    fitpath = attr.fitpath
    tabfile = tools.set_file('txt', dt_type, mode, tag,
                             prefix=prefix, extbase=fitpath)

    if os.access(tabfile, os.F_OK):
        orgtabfile =  tools.set_file('org', dt_type, mode, tag,
                                     prefix=prefix, extbase=fitpath)
        tab = DHadTable(tabfile)
        tab.output_org(orgtabfile)
        abspath = os.path.join(attr.base)#, attr.analysis)
        orgtabfile = orgtabfile.replace(abspath, '../..')
        tablink = '#+INCLUDE: "%s"\n' % orgtabfile
        msg = '\n* %s \n  %s \n\n%s\n %s\n' % (
            modename, figlink, tablink, loglink)
    else:
        sys.stdout.write('File does not exist: %s \n' %tabfile)
        sys.stdout.write('Skipping mode %s ... \n' % str(mode))
        msg = '\n* %s \n Skipped.\n'  % modename
        
    return msg

def sqrt_fig_mode(tag, dt_type, mode, label):
    if tag == 'single':
        modename = attr.modes[mode]['orgname']
    else:
        if mode == 'double_all_d0s':
            modename = 'Double all D0s'
        else:
            mode1 = mode[0]
            mode2 = mode[1]
            modename = '%s, %s' % (attr.modes[mode1]['orgname'],
                                   attr.modes[mode2]['orgnamebar'])
    prefix = 'dir_' + label
    rootfile = tools.set_file('root', dt_type, mode, tag,
                              prefix=prefix, extbase=attr.figpath)
    print rootfile
    #load_roofit_lib(dt_type)
    f = ROOT.TFile(rootfile)
    print f
    canvas = f.Get('canvas')
    print canvas

    canvas_1 = canvas.GetListOfPrimitives().FindObject('canvas_1')
    canvas_1.SetLogy(0)

    pdffile = rootfile.replace('.root', '.pdf')
    
    canvas.Print(pdffile)

    
    sys.exit()
