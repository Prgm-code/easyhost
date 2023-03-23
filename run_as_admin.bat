@echo off
powershell -Command "Start-Process 'cmd.exe' '/C python src\main.py' -Verb RunAs"
pause