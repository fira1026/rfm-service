#!/bin/sh

. ~/Envs/miniproj/bin/activate

uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload &

cd web/

./manage.py makemigrations
./manage.py migrate

exec ./manage.py runserver 0.0.0.0:8000
