gmail = {
	"user" : "example@gmail.com",
	"password" : "example"
}

services = {
	"proccessname" : "/some/path/to/script/script.sh"
}

email_to = ["email1@gmail.com", "email2@labworthy.com"]


email_body = """\

	Restarted the following proccesses succesfully:
		{services} at {timestamp}

"""