SLCV2020


Installing and running web service for the app:

Web Services are designed using Python as programming language and Django, DjangoRestFramework as web service processing frameworks.

Create fresh installation of Ubuntu 20.04 Operating System and execute the commands using root user

Install required packages

	apt-get update
	apt-get install python3
	apt-get install python3-pip
	apt-get install python3-venv
	apt-get install mysql mysql-client mysql-server
	apt-get install libmysqlclient-dev

Start and enable MySQL( Configuration of Mysql is not described in this document)

	systemctl start mysql
	systemctl enable mysql

Create Project directory and clone the code repository into it

	mkdir /project
	cd /project 
	git clone https://github.com/usandeepc/slcv2020.git
	cd /project/slcv2020

Install django and django rest framework in a virtual environment with pip
 
	python3 -m venv /slcv
	source /slcv/bin/activate
	pip install -r requirements.txt

Setup MySQL in django project
	
	Open settings.py file /project/slcv2020/codepro/settings.py and modify,
DATABASE section with the required ip and database name and username/password for mysql.



Initialize project 

	/slcv/bin/python  /project/slcv2020/manage.py makemigrations
	/slcv/bin/python  /project/slcv2020/manage.py migrate

Run the application

	/slcv/bin/python  /project/slcv2020/manage.py runserver 0.0.0.0:8080 

