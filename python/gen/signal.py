"""
Signal MC Generation Using Daemon 

"""

import sys
import time
from datetime import datetime
import logging
from tools.daemon import Daemon


__author__ = "Xin Shi <xs32@cornell.edu>"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2011 Xin Shi"
__license__ = "GPL"
__revision__ = "$Revision$"


class MyDaemon(Daemon):
	def run(self):
            while True:
                time.sleep(5)
                logfile = '/tmp/example.log'
                logging.basicConfig(filename=logfile,level=logging.DEBUG)
                logging.info('-'*50)
                logging.info(datetime.now())
                logging.debug('This message should go to the log file')
                logging.info('So should this')
                logging.warning('And this, too')


def main(opts, args):
    pidfile = '/tmp/daemon-example.pid'
    daemon = MyDaemon(pidfile)
    sys.stdout.write('dhad.gen.signal...\n')
    sys.stdout.write('Pid file in : %s \n' % pidfile)

    action = args[0]

    if action == 'start':
        daemon.start()
    elif action == 'stop':
        daemon.stop()
    else:
        raise NameError(action)


    
	
