"""
Script to create comparison table by dividing

"""
import os
import sys

import attr
import tools
from tools import DHadTable

__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):

    global _opts, _tabname
    _opts = opts
    _tabname = 'divide_' + '_'.join(args).replace('/', '_')

    if args[0] == 'yields':
	divide_yields(args[1:])
    else:
	raise NameError(args)

def divide_yields(args):

    if args[0] not in ['signal', 'data'] :
	raise NameError(args)

    variable = 'yields'
    rnd='.01'

    dt_type = args[0]
    tag = args[1]

    tab_A =  args[2]
    tab_B =  args[3]

    label_A, fitbase_A, prefix_A = tools.parse_tabname(_opts, tab_A) 
    label_B, fitbase_B, prefix_B = tools.parse_tabname(_opts, tab_B) 

    sys.stdout.write('dhad.tab : Divide %s of %s by %s:' %(
        variable, tab_A, tab_B))
    
    tab = DHadTable()
    namestyle = 'fname,fnamebar'
    tab.column_append_from_dict('Mode', namestyle)     

    tab.column_append_from_files(label_A, 'N1,N2', fitbase_A, prefix_A,
                                 dt_type, tag ,'txt', rnd='1.')
    tab.column_append_from_files(label_B, 'N1,N2', fitbase_B, prefix_B,
                                 dt_type, tag ,'txt', rnd='1.')
    tab.column_append_by_divide('%s/%s' %(label_A, label_B), label_A,
                                label_B, rnd=rnd, err_type='Indp')
    tab.output(_tabname)

