"""
DSkim  

"""
import os
import sys
import attr 
import cleog
import tools

from tools.filetools import CLEOGLOGFile
import chk 


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    sys.stdout.write('dhad.check.dskim ...\n')
    channel_names, arg = chk.parse_for_channel_names(args) 

    cmds = []
    for channel_name in channel_names:
        cmd = dskim_channel(opts, channel_name, arg)
        if cmd:
            cmds.append(cmd)

    if cmds:
        sys.stdout.write('-'*50+'\n')
        for cmd in cmds:
            sys.stdout.write(cmd)
  

def dskim_channel(opts, corname, arg=None):
    log_prifix = 'dskim'
    log_suffix = 'txt'

    logdir, jobsnum = cleog.get_logdir_jobsnum(arg)

    designed = attr.get_tag_numbers(corname)     

    sys.stdout.write('dhad.check.dskim.channel: %s ...\n' %corname )
    sys.stdout.write('| JobID | Designed | Generated | Diff (%)|\n')
    sys.stdout.write('|-------+----------+-----------+---------|\n')

    badjobs = []
    
    for job in jobsnum:
        logname = log_prifix + '-' + corname + '-' + str(
            job) + '.' + log_suffix
        logfile = os.path.join(logdir, logname)
        if opts.verbose > 0:
            sys.stdout.write('logfile: %s \n' %logfile)
        
        try:
            parsed = CLEOGLOGFile(logfile)
        except IOError:
            badjobs.append(job)
            continue

        generated = parsed.stream_event

        try:
            diff = (float(generated) - float(designed))*100./float(designed)
        except ValueError:
            diff = 'N/A'

        if parsed.processed_stops == 'N/A' or generated == 'N/A' or \
               abs(diff) > 1:
            badjobs.append(job)

        sys.stdout.write('| %s | %s | %s | %s |\n' % (
            job, designed, generated, diff))


    if badjobs:
        tasks = tools.numbers_to_string(badjobs)
        label = arg[0]
        cmd = 'dhad-%s gen dskim %s %s task %s \n' %(
            attr.version, corname, label, tasks)
        return cmd
       
 
