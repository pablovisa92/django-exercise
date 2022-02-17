# Concessionaire

## Prerequisites

- Install Python 3.6 or later
- Install [pip](https://pip.pypa.io/en/stable/)

## Getting started

```sh
python -m django --version
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py runserver
```

- Open localhost:8000 in your browser.

## Admin

```sh
python manage.py createsuperuser
```

## Run it with docker-compose in a GCP VM

1. Follow the instructions in (this guide)[https://cloud.google.com/community/tutorials/docker-compose-on-container-optimized-os].

2. After SSH to the VM, run the following commands:

```sh
git clone https://github.com/pablovisa92/django-exercise.git
cd django
```

3. Modify `app/settings.py` to point to a PostgreSQL database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

4. Copy the VM IP address to `app/settings.py`:

```python
ALLOWED_HOSTS = ['<IP>']
```

5. Start the app:

```sh
docker-compose up -d
```

6. Close the SSH session, copy the VM IP address and open it in your browser.

## References

### Features

- https://docs.djangoproject.com/en/4.0/
- https://tailwindcss.com, https://tailblocks.cc/, https://iconoir.com/ && https://favicon.io

### Deployment

- https://docs.docker.com/samples/django/
- https://cloud.google.com/community/tutorials/docker-compose-on-container-optimized-os

### API REST
- https://www.django-rest-framework.org
- https://www.geeksforgeeks.org/django-rest-api-crud-with-drf/