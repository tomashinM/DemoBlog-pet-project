#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser --noinput --skip-checks --username admin --email $SUPERUSER_EMAIL
python manage.py search_index --populate
# python manage.py test --keepdb


case $DJANGO_DEBUG in
    "True")
        python manage.py runserver 0.0.0.0:8000
        ;;
    "False")
        gunicorn config.wsgi:application --workers 3 --bind 0.0.0.0:8000
        ;;
esac
