"""
Check Ntuple  

"""
import os
import sys
import attr 
import cleog
import tools

from tools.filetools import CLEOGLOGFile
from tools import get_files_with_commonname
import chk 

__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    global _opts
    _opts = opts

    if args[0] == 'data':
        ntuple_data(args[1:])
    elif args[0] == 'generic':
        ntuple_generic(args[1:])
    else:
        ntuple_mc(args)
  
    
def ntuple_data(args):
    label = args[0]
    sys.stdout.write('dhad.check.ntuple data %s ...\n' %label )
    sys.stdout.write('| Dataset |  Processed | Stream event |\n')
    sys.stdout.write('|---------+------------+--------------|\n')

    numbers = attr.get_dataset_numbers(label)

    datasets = []
    for num in numbers:
        dataset = 'data' + num
        datasets.append(dataset)

    for dataset in datasets:
        ntuple_dataset(dataset)
    

def ntuple_mc(args):
    sys.stdout.write('dhad.check.ntuple MC ...\n')

    sys.stdout.write('|  Channel     |  Designed | Generated | Diff (%) |\n')
    sys.stdout.write('|--------------+-----------+-----------+----------|\n')
    
    channel_names, arg = chk.parse_for_channel_names(args) 

    for channel_name in channel_names:
        ntuple_channel(channel_name, arg)

def ntuple_channel(corname, arg=None):
    log_prifix = 'dtuple'
    log_suffix = 'txt'

    label = arg[0]
    if '281ipb' in label:
        jobs = 10
    elif '537ipb' in label:
        jobs = 20
    else:
        raise NameError(label)

    tag_numbers = attr.get_tag_numbers(corname)     
    designed = float(tag_numbers)*jobs

    logdir, jobsnum =  cleog.get_logdir_jobsnum(arg, 'ntuple')
    logname = log_prifix + '-' + corname +  '.'  +  log_suffix
    logfile = os.path.join(logdir, logname)
    parsed = CLEOGLOGFile(logfile)

    generated = parsed.stream_event

    try:
        diff = (float(generated) - float(designed))*100./float(designed)
    except ValueError:
        diff = 'N/A'

    sys.stdout.write('| %s | %s | %s | %s |\n' % (
        corname, designed, generated, diff))
    

def ntuple_dataset(dataset):
    log_prifix = 'dtuple'
    log_suffix = 'txt'

    logdir = os.path.join(attr.base, 'dat', 'data', attr.src)
    logname = log_prifix + '-' + dataset +  '.'  +  log_suffix
    logfile = os.path.join(logdir, logname)
    parsed = CLEOGLOGFile(logfile)
    sys.stdout.write('| %s | %s | %s |\n' % (
        dataset, parsed.processed_stops, parsed.stream_event))

def ntuple_generic(args):
    logdir = os.path.join(attr.base, 'dat', 'generic', attr.src)
    comname = '_'.join(args)

    if '281ipb' in comname:
        comname = comname.replace('281ipb', 'data3')
    
    if '537ipb' in comname:
        comname = comname.replace('537ipb', 'data4')
    
    log_suffix = 'txt'
    logfiles = get_files_with_commonname(logdir, comname, log_suffix)

    for logname in logfiles:
        logfile = os.path.join(logdir, logname)
        parsed = CLEOGLOGFile(logfile)
        sys.stdout.write('| %s | %s | %s |\n' % (
            logname, parsed.processed_stops, parsed.stream_event))

