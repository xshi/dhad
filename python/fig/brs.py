"""
Module for plotting figures for Branching Fractions 

"""

import os
import sys
import attr 
from tools import set_file, DHadTable, parse_result, \
     process_cmd, eps2pdf, eps2png
from tools.filetools import UserFile 
import shutil
import pexpect

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2010 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):

    if len(args) == 3:
        brsfile = create_brsfile_three(args)
    elif len(args) == 2:
        brsfile = create_brsfile_two(args)
    else:
        raise NameError(args)
    
    brspath, brsname = os.path.split(brsfile)
    os.chdir(brspath)

    figname = brsname.replace('.mnf', '.eps')

    p = pexpect.spawn ('mn_fit')
    p.expect ('Give screen device name')
    p.sendline ('\n')
    p.expect ('MN_CMD> ')
    p.sendline ('exec %s' %brsname)

    if len(args) == 3:
        p.expect ('any character to skip')
        p.sendline ('\n')
    
    p.expect ('End of Macro %s' %brsname)
    p.sendline ('\n')
    p.expect ('MN_CMD> ')
    p.sendline ('quit')

    shutil.copyfile('plot.eps', figname)
    eps2pdf(figname)
    eps2png(figname)
    sys.stdout.write('Save as %s/%s \n' %(brspath, figname))


def create_brsfile_three(args):
    comname = '_'.join(args)
    comname = comname.replace('.', '_')

    brsfile = set_file(extbase=attr.srcmnfpath, comname=comname, ext='mnf')
    brs = UserFile()
    header = r'''
set def
del 0
dep nmodes = 9

'''

    brs.append(header)

    label_0, content_0 = get_brs(args[0])

    label_1, content_1 = get_brs(args[2])
    label_2, content_2 = get_brs(args[1])
        
    brs.extend(content_0)
    brs.extend(content_1)

    hmin = 0.4
    hmax = 1.6
    xleft = 0.45
    textsize = 0.45

    if args[0] == 'pdg2010':
        hmin = 0.85
        hmax = 1.10
        xleft = 0.86
        
    trunk = r'''
exec colors
dep yoffset = -0.15
exec pdgCompareMany %s %s white mustard burgundy "%s" 4 "%s" 8

! Add another set of data points
rename 1 11
rename 2 12

''' % (hmin, hmax, label_0, label_1)
 
    brs.append(trunk)
    brs.extend(content_0)
    brs.extend(content_2)
        
    footer = r'''
dep yoffset = 0.15
exec pdgCompareMany %s %s white mustard burgundy "%s" 3 "%s" 6.5

over 11 -60/lavender
over 12 -60/lavender

key
1
new
1000
%s
13 17.5 0.4 0 left cm -2000 lavender 3 0.01 black

draw line 1 black 1 plot
%s, -3.5
%s, -3.5


! xleft is the x position of the mode label in plot units
dep xleft = %s
dep textsize = %s

exec pdgCompareComment 1 xleft textsize "'K^-![p]^+'"
exec pdgCompareComment 2 xleft textsize "'K^-![p]^+![p]^0!'"
exec pdgCompareComment 3 xleft textsize "'K^-![p]^+![p]^-![p]^+!'"
exec pdgCompareComment 4 xleft textsize "'K^-![p]^+![p]^+!'"
exec pdgCompareComment 5 xleft textsize "'K^-![p]^+![p]^+![p]^0!'"
exec pdgCompareComment 6 xleft textsize "'K^0?S![p]^+!'"
exec pdgCompareComment 7 xleft textsize "'K^0?S![p]^+![p]^0!'"
exec pdgCompareComment 8 xleft textsize "'K^0?S![p]^+![p]^-![p]^+!'"
exec pdgCompareComment 9 xleft textsize "'K^-!K^+![p]^+!'"

hard epost
'''  % (hmin, hmax, label_0, label_2, label_1, hmin, hmax, xleft, textsize)
    brs.append(footer)
    brs.output(brsfile)
    return brsfile


def get_brs(arg):
    if arg == 'pdg2004':
        label = 'PDG04'
        content = attr.brs_pdg2004
    elif arg == 'pdg2010':
        label = 'PDG10'
        content = attr.brs_pdg2010
    elif arg in ['281ipbv0', '818ipbv12.2']:
        label = 'CLEO %s pb^-1' % arg.split('ipb')[0]
        content = get_brs_from_file(arg)
    else:
        raise NameError(arg)
    return label, content


def get_brs_from_file(label):
    tab = DHadTable()
    bffilename = 'bf_stat_sys'

    bffile = os.path.join(attr.brfpath, label, bffilename)
    tab.column_append(parse_result(bffile, 'paras'), 'Parameters')
    tab.column_append(parse_result(bffile, 'value'), 'value')
    tab.column_append(parse_result(bffile, 'stat'),  'stat')
    tab.column_append(parse_result(bffile, 'syst'),  'syst')
    tab.rows_delete(['Parameters', 'ND0D0Bar', 'ND+D-'])

    content = []
    n = 0
    for row in tab.data:
        n += 1
        line = 'exec addData %s %s %s %s \n' %(
            n, row[1], row[2], row[3])
        content.append(line)
    return content


def create_brsfile_two(args):
    comname = '_'.join(args)
    comname = comname.replace('.', '_')

    brsfile = set_file(extbase=attr.srcmnfpath, comname=comname, ext='mnf')
    brs = UserFile()
    header = r'''
set def
del 0
dep nmodes = 9

'''

    brs.append(header)

    label_0, content_0 = get_brs(args[0])

    label_1, content_1 = get_brs(args[1])
    #label_2, content_2 = get_brs(args[1])
        
    brs.extend(content_0)
    brs.extend(content_1)

    hmin = 0.4
    hmax = 1.6
    xleft = 0.45
    textsize = 0.45

    if args[0] == 'pdg2010':
        hmin = 0.85
        hmax = 1.10
        xleft = 0.86
        
    trunk = r'''
exec colors
dep yoffset = -0.15
exec pdgCompareMany %s %s white mustard burgundy "%s" 4 "%s" 12


''' % (hmin, hmax, label_0, label_1)
 
    brs.append(trunk)
    #brs.extend(content_0)
    #brs.extend(content_2)
        
    footer = r'''
key
1


draw line 1 black 1 plot
%s, -3.5
%s, -3.5


! xleft is the x position of the mode label in plot units
dep xleft = %s
dep textsize = %s

exec pdgCompareComment 1 xleft textsize "'K^-![p]^+'"
exec pdgCompareComment 2 xleft textsize "'K^-![p]^+![p]^0!'"
exec pdgCompareComment 3 xleft textsize "'K^-![p]^+![p]^-![p]^+!'"
exec pdgCompareComment 4 xleft textsize "'K^-![p]^+![p]^+!'"
exec pdgCompareComment 5 xleft textsize "'K^-![p]^+![p]^+![p]^0!'"
exec pdgCompareComment 6 xleft textsize "'K^0?S![p]^+!'"
exec pdgCompareComment 7 xleft textsize "'K^0?S![p]^+![p]^0!'"
exec pdgCompareComment 8 xleft textsize "'K^0?S![p]^+![p]^-![p]^+!'"
exec pdgCompareComment 9 xleft textsize "'K^-!K^+![p]^+!'"

hard epost
'''  % (hmin, hmax, xleft, textsize)
    brs.append(footer)
    brs.output(brsfile)

    return brsfile
