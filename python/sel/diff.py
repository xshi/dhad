"""
Script to diff table

"""
import os
import sys
import ROOT 
import attr
import tools
import yld
import diff

__author__ = "Xin Shi <xs32@cornell.edu>"
__revision__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Xin Shi"
__license__ = "GNU GPL"


def main(opts, args):
    global _opts, _tabname
    _opts = opts
    _tabname = 'diff_' + '_'.join(args).replace('/', '_')
    function = getattr(diff, args[0])
    return function(args[1:])

def events(args):
    parsed = yld.parse_args(args)
    datatype  = parsed[0]
    tag       = parsed[1]
    modes     = parsed[2]
    label_A   = parsed[3]
    label_B  = args[3]

    for mode in modes:
        unique_file_A = get_unique_file(datatype, mode, label_A)
        unique_file_B = get_unique_file(datatype, mode, label_B)

        inputfile_A, outputfile_A = get_input_output_file(
            datatype, mode, label_A, 'sel/diff/events/%s' %label_B)

        inputfile_B, outputfile_B = get_input_output_file(
            datatype, mode, label_B, 'sel/diff/events/%s' %label_A)

        unique_file_A = get_unique_file(datatype, mode, label_A)
        unique_file_B = get_unique_file(datatype, mode, label_B)

        source = os.path.join(attr.srcselpath, 'DNTClass.C')

        ROOT.gROOT.ProcessLine('.L %s' % source )
        ROOT.gROOT.ProcessLine('DNTClass a("%s", "%s")'
                               %(inputfile_A, outputfile_A))
        ROOT.gROOT.ProcessLine('a.Skim("%s")' %unique_file_A)
        sys.stdout.write('Save as %s \n' % outputfile_A)        

        ROOT.gROOT.ProcessLine('DNTClass b("%s", "%s")'
                               %(inputfile_B, outputfile_B))
        ROOT.gROOT.ProcessLine('b.Skim("%s")' %unique_file_B)
        sys.stdout.write('Save as %s \n' % outputfile_B)


def get_unique_file(datatype, mode, label):
    evtname = '%s_%s_unqiue_%s.evt' %(datatype, mode, label)
    evtpath = os.path.join(attr.datpath, 'evt', label, 'events')
    unique_file = os.path.join(evtpath, evtname)
    return unique_file
    

def get_input_output_file(datatype, mode, label, outputdir):   
    datpath = attr.datpath
    if datatype == 'signal':
        inputname = mode+'.root'
    elif datatype == 'data':
        inputname = '*.root'
    else:
        raise NameError(datatype)
    outputname = mode+'.root'
    inputpath = os.path.join(datpath, datatype, label)
    outputpath = os.path.join(inputpath, outputdir)
    inputfile = os.path.join(inputpath, inputname)
    outputfile = tools.check_and_join(outputpath, outputname)

    return inputfile, outputfile

    
