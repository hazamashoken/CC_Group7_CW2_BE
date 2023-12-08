#!/bin/bash

python manage.py migrate \
&& python manage.py createsuperuser --noinput 

hypercorn app.asgi:application -b 0.0.0.0:8000