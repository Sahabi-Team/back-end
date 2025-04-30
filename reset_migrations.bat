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

REM Make migrations
echo Making migrations...
python manage.py makemigrations

REM Apply migrations
echo Applying migrations...
python manage.py migrate

echo Done!
pause
