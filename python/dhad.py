#!/usr/bin/env python
"""
Main script for D-Hadronic analysis.

"""

import sys
import optparse
import attr


__author__ = "Xin Shi <xs32@cornell.edu>"
__version__ = "v2"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2013 Xin Shi"
__license__ = "Python"


def print_sep(width=35):
    sys.stdout.write('-'*width+'\n')

def main():
    print_sep()
    sys.stdout.write('    Version : %s    \n' % __version__)
    sys.stdout.write('      CLEOG : %s    \n' % attr.cleog)
    sys.stdout.write('      PASS2 : %s    \n' % attr.pass2)
    sys.stdout.write('      DSKIM : %s    \n' % attr.dskim)
    sys.stdout.write('     NTuple : %s    \n' % attr.ntuple)
    print_sep()

    parser = optparse.OptionParser()
    parser.add_option("-d", dest="debug", default=False,
                      action="store_true", help="debug mode")
    parser.add_option("-s", dest="set", default=None,
                      help="set variables")
    parser.add_option("-t", dest="test", default=False,
                      action="store_true", help="test the code")
    parser.add_option("-v", dest="verbose", default=0,
                      help="verbose level")
    parser.add_option("--qsub", dest="qsub", default=False,
                      action="store_true", help="qsub job")
    (opts, args) = parser.parse_args()

    if opts.qsub:
        command = sys.argv[0].split('/')[-1] +' '+  ' '.join(sys.argv[1:])
        command = command.replace('--qsub', '')
        from tools import qsub_cmd
        return qsub_cmd(command, opts.test)

    if args == []:
        sys.stdout.write('Please use -h for help.\n')
        return

    module_name = args[0]
    module = __import__(module_name)
    module.main(opts, args[1:])

if __name__ == '__main__':
    main()

