# Refbooks
Web-application which helps you to create and read refbooks.  
[![Python CI](https://github.com/Perceptor89/refbooks/actions/workflows/pyci.yml/badge.svg)](https://github.com/Perceptor89/refbooks/actions/workflows/pyci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/3b87494bf2d02ece8714/maintainability)](https://codeclimate.com/github/Perceptor89/refbooks/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3b87494bf2d02ece8714/test_coverage)](https://codeclimate.com/github/Perceptor89/refbooks/test_coverage)

---

## Local installation:
1. Clone repository:
```bash
git clone git@github.com:Perceptor89/refbooks.git
```

2.  Rename '**.env.exaple**' to '**.env**' and fill parameters there.

3. Install virtual environment and dependencies. I recommend to use poetry.

```bash
poetry install
```

4. Make migrations:

```bash
[poetry run] python manage.py makemigrations
[poetry run] python manage.py migrate
```

5. To launch the app:

```bash
[poetry run] python manage.py runserver
```
6. Do not forget to create superuser:

```bash
[poetry run] python manage.py createsuperuser
```

Usually it runs from: http://127.0.0.1:8000/  
Check admin panel: http://127.0.0.1:8000/admin/  
See API in Swagger: http://127.0.0.1:8000/swagger/

---
## Used technologies:

| Tool                                                                     | Description                                                                                                           |
|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [Django framework](https://www.djangoproject.com/)                                 | "The web framework for perfectionists with deadlines."                                                   |
| [Django REST framework](https://www.django-rest-framework.org)                                     | "Django REST framework is a powerful and flexible toolkit for building Web APIs."                                                             |
---
## Questions and suggestions:
<andreyfominykh@gmail.com>