import time
import grp
import pwd
import argparse
import sys
from daemon import runner
import subprocess
import logging
import re
import imaplib
import socket
import ssl
import email
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from subprocess import call
from subprocess import Popen, PIPE
from config import services as apps


class MonitorService(object):

	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/null'
		self.stderr_path = '/tmp/monitorservice.log'
		self.pidfile_path = '/tmp/daemon.pid'
		self.pidfile_timeout = 1

		# Command and service list
		self.servicelist = apps.keys()

		# Set logging level
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)


	def run(self):
		while True:
			for service in self.servicelist:
				if self.isProcessRunning(service):
					self.logger.info("Found service: {}".format(service))
					self.logger.info('Executing: {}'.format(apps[service]))
					call(apps[service], shell=True)

			time.sleep(1)

	def findProcess(self, processId):
		ps = subprocess.Popen("ps aux | grep {} | grep -v grep | grep -v monitorservice".format(processId), shell=True, stdout=subprocess.PIPE)
		output = ps.stdout.read()
		ps.stdout.close()
		ps.wait()
		return output

	def isProcessRunning(self, processId):
		output = self.findProcess(processId)
		self.logger.debug(output)
		if re.search(processId, output) is None:
			return False
		else:
			return True

if __name__ == '__main__':
	
	app = MonitorService()
	daemon_runner = runner.DaemonRunner(app)
	daemon_gid = grp.getgrnam('root').gr_gid
	daemon_uid = pwd.getpwnam('root').pw_uid
	daemon_runner.daemon_context.gid = daemon_gid
	daemon_runner.daemon_context.uid = daemon_uid
	daemon_runner.do_action()