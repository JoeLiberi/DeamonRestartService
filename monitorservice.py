import time
import datetime
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
import config


class MonitorService(object):

	def __init__(self):
		self.pidfile_timeout = 1
		self.stdin_path = '/tmp/monitorservice.log'
		self.stdout_path = '/tmp/monitorservice.log'
		self.stderr_path = '/tmp/monitorservice.log'
		self.pidfile_path = '/tmp/daemon.pid'
		self.gmailuser = config.gmail["user"]
		self.gmailpassword = config.gmail["password"]
		self.webapp = config.webapp

		# Command and service list
		self.servicelist = apps.keys()

		# Set logging level
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)


	def run(self):
		while True:
			for service in self.servicelist:
				if not self.isProcessRunning(service):
					self.logger.info("Found service: {}".format(service))
					self.logger.info('Executing: {}'.format(apps[service]))
					call(apps[service])
					self.sendmail(service)

				else:
					self.logger.debug("{} is running".format(service))

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

	def connecttogmail(self):
		try:
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(self.gmailuser, self.gmailpassword)
			self.logger.info("Succesfully logged into Gmail")

			return server
		except:  
			self.logger.info("Could not connect to gmail")
			return None

	def sendmail(self, service):
		email_text = """\
		Subject: {subject}


		From: {sent_from}  
		To: {to}  


		{body}


		"""

		sent_from = self.gmailuser  
		to = ", ".join(config.email_to)
		subject = 'Process Monitor'

		# Create timestamp
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		body = config.email_body.format(service=service, timestamp=st, webapp=self.webapp)
		text = email_text.format(sent_from=sent_from, to=to, subject=subject, body=body)

		s = self.connecttogmail()
		self.logger.info("Sending mail.....")
		s.sendmail(sent_from, to, text)
		s.close()
		self.logger.info("mail sent")


if __name__ == '__main__':
	
	app = MonitorService()
	daemon_runner = runner.DaemonRunner(app)
	daemon_runner.do_action()