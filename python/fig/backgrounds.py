"""
Module for Backgrounds Study

"""

import os
import sys
import tools
import attr

from tools.filetools import UserFile
from tools import DHadTable, get_modekey
from yld import parse_args


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    parsed = parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label     = parsed[3]

    figname = '_'.join(args).replace('/', '_')

    org = UserFile()
    org.append(attr.fig_web_header)

    if 'allinone' in opts.set:
        msg = create_fig(datatype, label)
        org.append(msg)
    else:
        for mode in modes:
            msg = create_fig_mode(tag, datatype, mode, label)
            org.append(msg)
        
    org.append(attr.fig_web_footer)
    orgname = '%s.org' % figname
    orgfile = os.path.join(attr.figpath, orgname)
    org.output(orgfile)
    tools.org_export_as_html(orgfile)

    orglink = '[[./%s/fig/%s][figure]]' %(attr.analysis, orgname)
    sys.stdout.write('\n%s\n\n' % orglink)


def create_fig_mode(tag, datatype, mode, label):
    if tag != 'single':
        raise NameError(tag)
        
    comname = '%s_%s' %(datatype.replace('/', '_'), mode)

    epspath = os.path.join(attr.figpath, label)    
    epsname = '%s.eps' % comname
    epsfile = os.path.join(epspath, epsname)

    txtpath = os.path.join(attr.fitpath(), label)    
    txtname = '%s.txt' % comname
    txtfile = os.path.join(txtpath, txtname)

    pdflink = './%s/%s.pdf' %(label, comname)
    pnglink = './%s/%s.png' %(label, comname)
    loglink = '[[../log/%s/backgrounds/%s.txt][log]]' %(label, comname)

    figlink = '[[%s][%s]]' %(pdflink, pnglink)

    modename = tools.get_orgname_from_fname(mode)

    tablink = ''
    if os.access(txtfile, os.F_OK):
        orgtabfile = txtfile.replace('.txt', '.org')
        tab = DHadTable(txtfile)
        tab.output_org(orgtabfile)

        abspath = os.path.join(attr.base, attr.analysis)
        orgtabfile = orgtabfile.replace(abspath, '..')

        tablink = '#+INCLUDE: "%s"\n' % orgtabfile

    msg = '\n* %s \n  %s \n\n%s\n %s\n' % (
        modename, figlink, tablink, loglink)

    return msg

def create_fig(datatype, label):
    comname = '%s_background' %(datatype.replace('/', '_'))
    pdflink = './%s/%s.pdf'  % (label, comname)
    pnglink = './%s/%s.png'  % (label, comname)
    figlink = '[[%s][%s]]' %(pdflink, pnglink)

    logname = '%s_allinone.txt' % datatype.replace('/', '_')
    loglink = '[[../log/%s/backgrounds/%s][log]]' %(label, logname)

    msg = '%s\n\n %s\n' % (figlink, loglink)
    return msg

