@echo off
start python manage.py runserver 0.0.0.0:8000
timeout /t 3
powershell -command "Start-Process 'http://127.0.0.1:8000/incident'"