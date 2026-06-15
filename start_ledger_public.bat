@echo off
cd /d "%~dp0"
py -m pip install -r requirements-google.txt
py server.py --setup --open
