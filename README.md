# DaemonRestartService

A Python daemon that checks to make sure a process or multiple processes are running. If it finds a process that is not running it executes the bash script configured in "config.py"


## Setting up config.py

Take a look at the config_example.py file replace the gmail user and password with the username and password of the account that you would like the software to use. The "email_to" list is a list of email addresses that will recieve the email updates. The "email_body" is the body of the email, you can edit anything that not in brackets. If you edit the stuff in brackets the whole thing will break, so dont do that.
