# COEP-DORM

COEP-DORM is hostel management system specifically designed for COEP college students to get admission in Hostel wihtout manual effor

### Getting Started

A customize website which helps customer to aid customer to book time slot and it also allows the manager to provide room on rent for particular time slot. 


### Features

##### Types Of User:
 - Student
 - Admin
    
##### Admin
 - The admin can fetch all the details of the applicants, from the main college database containing all the infromation.
 - The admin just need to specify total intake per branch and the number of rooms available.
 - All the processing of querying according to year, branch ,CGPA and category reservation,will be done by the designed algorithm.

##### Student
 - Students just need to register with a single click, without providing all the details again.
 - Students get to know thier status information by viewing their profile after logging in.
 - Selected students can specify their roommates preferences,which will be allocated purely on merit basis.
 - The room allocation proceeds by considering branches in an alphabetical sequence and then according to merit.
 - Once room allocated stuudents can pay their fees with online transaction either through card, netbanking or remaining payment method also added.


### Prerequisites
```
Python 3 and higher version.
Django 2.1.7
```

### Installing
1. How to install virtualenv
```
$ pip3 install virtualenv 
$ virtualenv -p /usr/bin/python3 env
$ source env/bin/activate
```

2. Installing requirements
```
$ pip3 install -r requirement.txt
```

3. Change directory to book_room
```
$ cd book_room
$ python3 manage.py makemigrations accounts
$ python3 manage.py makemigrations manager
$ python3 manage.py makemigrations customer
$ python3 manage.py migrate
$ python3 manage.py collectstatic
```

4. Run the application, running on localhost.
```
$ python3 manage.py runserver
```
open [localhost](http://127.0.0.1:8000/) in browser.

5. Testing Reset Password feature using Django Email Server
* Starting the email server in another terminal
```
python3 -m smtpd -n -c DebuggingServer localhost:1025
```
* open [Reset Password](http://127.0.0.1:8000/accounts/password_reset/) in browser
* Enter email address to reset password
* open terminal to check for email.

### Running the tests
```
$ python3 manage.py test
```
