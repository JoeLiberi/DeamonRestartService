import time
import grp
import pwd
import argparse
import sys
from daemon import runner
import subprocess
import logging
import re


class MonitorService(object):

	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/null'
		self.stderr_path = '/tmp/monitorservice.log'
		self.pidfile_path = '/tmp/daemon.pid'
		self.pidfile_timeout = 1

		# Command and service list
		self.commandlist = []
		self.servicelist = []

		# Set logging level
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)

		# Read the config file
		with open('config.txt', 'r') as file:
			for line in file:
				self.servicelist.append(line)
				command = ['systemctl', "stop", "{}".format(line.strip('\n'))]
				self.commandlist.append(command)

	def run(self):
		while True:
			for service, cmd in zip(self.servicelist, self.commandlist):
				if self.isProcessRunning(service):
					self.logger.info("Found service: {}".format(service))
					self.logger.info('Executing: {}'.format(cmd))
					subprocess.call(cmd, shell=True)


			time.sleep(1)

	def findProcess(self, processId):
		ps = subprocess.Popen("ps aux | grep {} | grep -v grep".format(processId), shell=True, stdout=subprocess.PIPE)
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
	daemon_gid = grp.getgrnam('m4punk').gr_gid
	daemon_uid = pwd.getpwnam('m4punk').pw_uid
	daemon_runner.daemon_context.gid = daemon_gid
	daemon_runner.daemon_context.uid = daemon_uid
	daemon_runner.do_action()