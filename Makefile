run:
	@echo "No defaults!"

# Make migrations
mm:
	cd app &&\
	env $$(cat ../.env.local) python manage.py makemigrations

# Migrate
m:
	cd app &&\
	env $$(cat ../.env.local) python manage.py migrate

# Create superuser
su:
	cd app &&\
	env $$(cat ../.env.local) python manage.py createsuperuser

# Tunnels using cloudflared
tunnel:
	docker run --rm --net=host cloudflare/cloudflared:latest tunnel run --token $(CF_TOKEN)

# Run celery worker
run-worker:
	cd app &&\
	poetry run celery -A app worker -l INFO -E

# Run celery scheduler
run-beat:
	cd app &&\
	poetry run celery -A app beat -l INFO

# Generate requirements.txt
req:
	poetry export -f requirements.txt --output requirements.txt

# Build docker image
build:
	docker build -t datagov-backend-main:latest .

# Run docker image
run-docker:
	docker run --rm -p 8888:8000 --env-file .env.local datagov-backend-main

# Drop databases
drop-tables:
	@read -p "Enter Y to confirm dropping all tables: " confirm; \
	if [ $$confirm = "Y" ]; then \
		psql "dbname=postgres host=db port=5432 user=postgres password=postgres" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" ;\
		exit 0; \
	fi; \

# Run hypercorn WSGI
hypercorn:
	cd app &&\
	hypercorn app.asgi:application --workers 4 -b 0.0.0.0:8000

# Run tests
test:
	cd app &&\
	python manage.py test --parallel

frontend-test:
	cd playground/frontend-test &&\
	bash run_frontend.sh

django-default-models:
	cd app &&\
	env $$(cat ../.env.local) python manage.py init_default_data

pytest:
	cd tests && \
	pytest -n auto -vv

init-git:
	git config core.fileMode false
	git config --global --add safe.directory /workspaces/backend-main

# Byebye db, recreate db and init default data, dummy data
re-init:
	psql "dbname=postgres host=db port=5432 user=postgres password=postgres" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	cd app && env $$(cat ../.env.local) python manage.py migrate
	cd app && env $$(cat ../.env.local) python manage.py init_dummy

dev-tunnel:
	cloudflared tunnel --url http://localhost:8000

re-run: bye-db run hypercorn
