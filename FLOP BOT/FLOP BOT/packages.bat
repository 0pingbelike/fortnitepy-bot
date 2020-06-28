@echo off
ECHO Installing Required Packages, this will take a minute...
TIMEOUT 3

py -3 -m pip install -U -r requirements.txt

ECHO Finished installing the packages
ECHO Close this window and run “Start Bot.bat”
PAUSE