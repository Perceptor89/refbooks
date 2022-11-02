MANAGE := poetry run python manage.py


run:
	$(MANAGE) runserver

check:
	$(MANAGE) check

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

test:
	$(MANAGE) test
	
shell:
	$(MANAGE) shell

lint:
	poetry run flake8 refbooks_keeper

coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml
	poetry run coverage report

requirements:
	poetry export -f requirements.txt --output requirements.txt