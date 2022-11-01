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
	poetry run flake8 refbooks_keeper/refbooks/