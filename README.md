# UR-Spaces
 Website project for CS 476

Created by:
clg875 = Catherine Grant,
bobby7197 = Andrew Doidge,
Eileen12345678 = Eileen Guo,
xfy246 = Xialei Fang,
maj448 = Marissa Joyce

#Running the website is in URSpaces
cd URSpaces

#required files
pip install django
pip install django-crispy-forms
pip install django-resized
pip install  Pillow
pip install crispy-bootstrap4

#to make migrations
py manage.py makemigrations
py manage.py migrate

#to run server
py manage.py runserver

Test moderator:
username: admin1
password: test1234

Test user:
username: johndoe1
password: Test1234!