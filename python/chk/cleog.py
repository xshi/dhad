"""
Check CLEOG logs 

"""

import os
import sys
import distutils.version

import attr
import tools
from tools.filetools import CLEOGLOGFile
import chk 


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


def main(opts, args):
    #global _opts
    #_opts = opts

    sys.stdout.write('dhad.check.cleog ...\n')

    channel_names, arg = chk.parse_for_channel_names(args) 

    cmds = []
    for channel_name in channel_names:
        cmd = cleog_channel(channel_name, arg)
        if cmd:
            cmds.append(cmd)
    
    if cmds:
        sys.stdout.write('-'*50+'\n')
        for cmd in cmds:
            sys.stdout.write(cmd)

def cleog_channel(corname, arg=None):
    log_prifix = 'cleog'
    log_suffix = 'txt'

    logdir, jobsnum = get_logdir_jobsnum(arg)

    designed = attr.get_tag_numbers(corname)     

    sys.stdout.write('dhad.check.cleog.channel: %s ...\n' %corname )
    sys.stdout.write('| JobID | Designed | Generated | Diff (%)|\n')
    sys.stdout.write('|-------+----------+-----------+---------|\n')

    badjobs = []

    for job in jobsnum:
        logname = log_prifix + '-' + corname + '-' + str(
	    job) + '.' +  log_suffix
        logfile = os.path.join(logdir, logname)
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
        cmd = 'dhad-%s gen cleog %s %s task %s \n' %(attr.version, corname,
                                                     label, tasks)
        return cmd


def get_logdir_jobsnum(arg, opt=None):
    src = distutils.version.StrictVersion(attr.version)
    if src >= distutils.version.StrictVersion(
	'10.1') and src < distutils.version.StrictVersion('10.2') :
        logdirname = 'log'+'_' + attr.cleog + '_' + attr.pass2 

        logdir  = os.path.join(attr.base, 'dat/signal', attr.version, logdirname)
        if opt and opt == 'ntuple':
            if arg != None:
                logdir = os.path.join(logdir, arg[0])
        jobsnum = range(1,31)

    elif src >= distutils.version.StrictVersion(
	'11.4') and src < distutils.version.StrictVersion('11.5') :
        logdirname = 'log'+'_' + attr.cleog + '_' + attr.pass2
        label = arg[0]
        logdir  = os.path.join(attr.datpath, 'signal', label, logdirname)

    else:
        raise ValueError(attr.version)

    if arg:
        label = arg[0]
        if '281ipb' in label:
            jobsnum = range(1,11)
        elif '537ipb' in label:
            jobsnum = range(11,31)
        elif '818ipb' in label:
            jobsnum = range(1,31)
            
        if len(arg) > 1 and arg[1] == 'task':
            task_id = arg[2]
            if '-' in task_id:
                task_begin =  int(task_id.split('-')[0])
                task_end   =  int(task_id.split('-')[1])+1
                jobsnum  = range (task_begin, task_end)
            else:
                jobsnum = task_id.split(',')

    return logdir, jobsnum

