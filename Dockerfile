# Use the official Python runtime image
# FROM python:3.13.3-slim-bookworm
FROM python:3.9-slim

# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN apt-get update && apt-get install -y python3-dev build-essential

RUN pip install --upgrade pip 
RUN pip install --upgrade pip setuptools wheel

# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container
COPY . /app/

RUN rm -f db.sqlite3

RUN rm -rf */__pycache__

RUN ls -la /app  

RUN python manage.py collectstatic
 
# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 