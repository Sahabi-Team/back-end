# Use the official Python runtime image
FROM python:3.13.3-slim-bookworm
 
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
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container
COPY . /app/

RUN rm -f db.sqlite3

# RUN rm -rf */migrations

RUN rm -rf */__pycache__

RUN ls -la /app  

# RUN python manage.py makemigrations authentication trainer_auth tests client_auth exercise workout analytics permissions opinions mentorship notification chat

# RUN python manage.py migrate

# RUN python manage.py add_exercise --count 20

# RUN python manage.py add_user --count 20

# RUN python manage.py collectstatic
 
# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 