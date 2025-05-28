@echo off
REM Stop on error
setlocal enabledelayedexpansion

REM List of apps
set apps=authentication trainer_auth tests client_auth exercise workout analytics permissions opinions mentorship

REM Delete migration files (except __init__.py)
for %%A in (%apps%) do (
    echo Deleting migrations for app %%A...
    rmdir /s /q %%A\migrations
    mkdir %%A\migrations
    echo. > %%A\migrations\__init__.py
)

REM Delete SQLite database (optional)
if exist db.sqlite3 (
    echo Deleting old database...
    del db.sqlite3
)

@REM REM Make migrations
@REM echo Making migrations...
@REM python manage.py makemigrations

@REM REM Apply migrations
@REM echo Applying migrations...
@REM python manage.py migrate

@REM echo Done!
@REM pause
