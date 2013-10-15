#!/usr/bin/env python

import os
import sys
import string

print 'THIS SCRIPT IS EXPERIMENTAL.'
print 'If there are any problems, contact Peter Onyisi (ponyisi@lns) and complain.'
print '-------------------------------'

print 'This script _must_ be run from the top-level directory of your processor.'
procname = os.path.basename(os.getcwd())
checkdir = os.path.join(os.getcwd(), procname)
header_files = ['TUPLE_DEFINITION', 'tuple_cxx_structure.h',
                'tuple_hbook_definition.h', 'tuple_root_definition.h']
if not os.access(checkdir, os.F_OK):
    print "I don't believe you are in this directory because then the directory"
    print checkdir
    print "ought to exist.  Exiting."
    sys.exit(1)
## header_files_withpath = map(lambda x: os.path.join(checkdir,x), header_files)
## #print header_files_withpath
## for i in header_files_withpath:
##     if not os.access(i, os.F_OK):
##         print 'Cannot find file', i
##         print 'Have you run genDefinitions.py?'
##         sys.exit(1)
## print 'It looks like the files I need are ready'
print
print 'I believe your processor is called', procname
print 'If this is NOT correct, cancel using Ctrl-C.  Else hit enter'
try:
    raw_input()
except KeyboardInterrupt, e:
    sys.exit(0)

print 'Please enter tuple class name'
tuplename = raw_input()
print 'I will create a tuple called', tuplename, '.  If this is NOT correct, '
print 'cancel using Ctrl-C.  Else hit enter'
try:
    raw_input()
except KeyboardInterrupt, e:
    sys.exit(0)
 
copy_files = [ 'SampleTuple.cc', 'SampleTuple.h' ]

for i in map(lambda x: os.path.join(os.getcwd(), '../CWNFramework/Test',
                                    x), copy_files):
    if not os.access(i, os.F_OK):
        print 'Cannot find', i
        sys.exit(1)
    else:
        fi = open(i, 'r')
        if os.path.basename(i) == copy_files[0]:
            fo = open(os.path.join('Class/', tuplename + '.cc'), 'w+')
        else:
            fo = open(os.path.join(procname, tuplename + '.h'), 'w+')
        for line in fi:
            n1line = line.replace('_REPLACE_BY_PROCDIR_', procname)
            n2line = n1line.replace('_REPLACE_BY_TUPLENAME_', tuplename)
            fo.writelines(n2line)
        fi.close(); fo.close()

print 'All done'
