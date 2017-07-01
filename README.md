# Flask Applications
 Flask Applications


### Steps to Install
 1. Install the dependencies.

 sudo apt-get install libmysqlclient-dev -y
 sudo apt-get install python-dev -y
 pip install --ignore-installed -r requirements.txt

2. Set up MySQL.

 sudo apt-get install mysql-server (Enter the password when prompted)
 
3. Check the status of the service. It should be running.

 service mysql status

4. Log in to MySQL and create a database named deployment.

 mysql -u root -p"<password>"
 create database demo;

5. Create Virtual Env if it is not created
    virtualenv venv
    
6. activate Virtual Env
   source venv/bin/activate
   
7. Install the requirement.txt
   pip install --ignore-installed -r requirements.txt

8. Export environment variables.

 export DB_HOST="127.0.0.1"
 export DB_USER="root"
 export DB_PASS="<password>"
  
9. Set up database.

 python db.py db init
 python db.py db migrate
 python db.py db upgrade
 python db.py seed

10. Run the application.

 python run.py
 
11. Go to the postman and test signup api which is given for test
    URL  : http://localhost/ums/api/v1/users
    POST : {
	"email":"sagarsalvi2011@gmail.com",
	"password":"Opcito@123"
	
 }
    Response : {
    "data": "",
    "message": "Your account has been successfully registered"
  }




