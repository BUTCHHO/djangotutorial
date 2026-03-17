export $(cat .env.local | grep -v '^#' | xargs)
python manage.py runserver