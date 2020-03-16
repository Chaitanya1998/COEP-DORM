# COEP-DORM

COEP-DORM Hostel Management System is designed to automate the entire process of getting admission to the hostel. It collects student information during registration and allocates room to the registered students and also provides feature of paying the fee through debit cards or other payment methods. It also takes into consideration all the factors such as branch, gender, caste-reservation, CGPA, etc. This system has been created to help the college and the student to easily register and use the system to allocate the room to the student. This system also generates the pdf which helps to retrieve the student details and helps to allocates the room based on the student's preference.

### Features

##### Types Of User:
 - Student
 - Admin
    
##### Admin
 - The admin can fetch all the details of the applicants, from the main college database containing all the information.
 - The admin needs to specify the total intake per branch and the number of rooms available.
 - Room allocation is given preference according to year, branch, CGPA and category reservation.

##### Student
 - Students need to register with a single click, without providing all the details again. Student data is fetched from the college database.
 - Students can know their status information by viewing their profile after logging in.
 - Selected students can provide their roommates' preferences, which will be allocated on first come first serve basis.
 - The room allocation proceeds by considering branch,  year, branch, CGPA and category reservation.
 - Once room allocated students can pay their fees with an online payment system through a card, net banking.

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

3. Change directory to COEP-DORM
```
$ cd COEP-DORM
$ python3 manage.py makemigrations app1
$ python3 manage.py migrate
$ python3 manage.py collectstatic
```

4. Run the application, on localhost.
```
$ python3 manage.py runserver
```
open [localhost](http://127.0.0.1:8000/) in browser.

### Running the tests
```
$ python3 manage.py test
```
