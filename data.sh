docker compose exec backend python manage.py makemigrations authentication trainer_auth tests client_auth exercise workout analytics permissions opinions mentorship notification chat

docker compose exec backend python manage.py migrate

docker compose exec backend python manage.py collectstatic

# docker compose exec backend python manage.py createsuperuser

docker compose exec backend python manage.py add_exercise --count 20

docker compose exec backend python manage.py add_user --count 20
