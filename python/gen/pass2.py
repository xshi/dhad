"""
Generate MCP2 

"""

import os
import sys
import commands
import subprocess

import attr
import cleog
from tools.filetools import UserFile
import gen


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"



def main(opts, args):
    sys.stdout.write('dhad.gen: Processing Pass2 ...\n')
    modes, label, tasks = gen.parse_for_modes_tasks(args)

    for mode in modes:
        pass2_mode(opts, mode, label, tasks)


def pass2_mode(opts, mode, label, tasks=[1]):
    sys.stdout.write('dhad.gen.pass2: Mode %s \n' %mode )
    sys.stdout.write('dhad.gen.pass2: Label %s \n' %label)
    sys.stdout.write('dhad.gen.pass2: Task %s \n' %tasks)

    jobtype = 'pass2'
    cleog.edit_fix_single_mode_list(opts, mode, label)
    cleog.check_and_copy_file(opts, label, 'mcp2.tcl')
    cleog.check_and_copy_file(opts, label, 'pass2-generic-array.sh')

    for task_id in tasks:
        if opts.set == 'interact':
            bash_file, logfile = cleog.create_bash_interact(
                jobtype, mode, task_id, label=label)
            if opts.test:
                sys.stdout.write(bash_file + '\n')
            else:
                subprocess.Popen(bash_file)
            return

        if opts.set == 'bg':
            bash_file, logfile = cleog.create_bash_interact(
                jobtype, mode, task_id, label=label)
            if opts.test:
                sys.stdout.write(bash_file + '\n')
                sys.stdout.write(logfile + '\n')
            else:
                sys.stdout.write('Save log as %s.\n' %logfile)
                process = subprocess.Popen(bash_file, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)
                f = UserFile()
                f.append(process.communicate()[0])
                f.output(logfile)

            return

        bash_file = cleog.create_bash_fix_mc_job(jobtype, label, task_id)
        if opts.test:
            sys.stdout.write(bash_file + '\n')
            continue

        output = commands.getoutput(bash_file)
        sys.stdout.write(output+ '\n')

