MANAGE := poetry run python manage.py


run:
	$(MANAGE) runserver

check:
	$(MANAGE) check

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	