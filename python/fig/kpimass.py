"""
Module for Kpimass Figures 

"""

import os
import sys
import tools
import attr

from tools.filetools import UserFile
from tools import DHadTable, get_modekey, parse_opts_set
from yld import parse_args


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    figname = 'kpimass_'+'_'.join(args[:-1]).replace('/', '_')

    org = UserFile()
    org.append(attr.fig_web_header)

    binbase = parse_opts_set(opts.set, 'binbase')
    binwidth =  parse_opts_set(opts.set, 'binwidth')
    numbins = parse_opts_set(opts.set, 'numbins')
    
    for i in xrange(numbins):
        lowmass = binbase+i*binwidth
        highmass = binbase+(i+1)*binwidth

        for mode in modes:
            msg = create_fig_mode(opts, tag, datatype, mode,
                                  lowmass, highmass, label)
            org.append(msg)
    
    org.append(attr.fig_web_footer)
    orgname = '%s.org' % figname
    orgfile = os.path.join(attr.figpath, label, orgname)
    org.output(orgfile, verbose=1)

    orglink = '[[./fig/%s/%s][figure]]' %(label, orgname)
    sys.stdout.write('\n%s\n\n' % orglink)

    tools.org_export_as_html(orgfile)


def create_fig_mode(opts, tag, datatype, mode, lowmass, highmass, label):
    modekey = tools.get_modekey(mode)
    comname = '%s_%s' %(datatype.replace('/', '_'), mode)
    
    prefix = 'dir_%s/kpimass/%s_%s' % (label, lowmass, highmass)
    epsfile = tools.set_file('eps', datatype, modekey, tag,
                            prefix=prefix, extbase=attr.figpath)
    
    txtfile = tools.set_file('txt', datatype, modekey, tag,
                            prefix=prefix, extbase=attr.fitpath)

    head, figname = os.path.split(epsfile)
    figname = figname.replace('.eps', '')

    subdir = 'kpimass/%s_%s' % (lowmass, highmass)
    pdflink = './%s/%s.pdf' %(subdir, figname)
    pnglink = './%s/%s.png' %(subdir, figname)
    
    loglink = '[[../../log/%s/%s/%s.txt][log]]' %(label, subdir, comname)
    figlink = '[[%s][%s]]' %(pdflink, pnglink)
    
    modename = tools.get_orgname_from_fname(mode)
    secname = 'Kpi mass: %s - %s' % (lowmass, highmass)
    tablink = ''
    if os.access(txtfile, os.F_OK):
        orgtabfile = txtfile.replace('.txt', '.org')
        tab = DHadTable(txtfile)
        tab.output_org(orgtabfile)
        tablink = '#+INCLUDE: "%s"\n' % orgtabfile

    msg = '\n* %s \n  %s \n\n%s\n %s\n' % (
        secname, figlink, tablink, loglink)
        
    return msg

