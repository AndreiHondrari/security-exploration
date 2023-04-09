# Slow HTTP Request Attack - Against WSGI

## Modes of operation

- wsgiref http server
- uwsgi
- gunicorn

### WSGIRef (sync only)

run `python -B 01_01_wsgiref_server.py`

### UWSGI (async by default?)

run `uwsgi --http :7777 --workers 1 --threads 1 --wsgi-file wsgi_app.py`

### Gunicorn sync

run `gunicorn --bind :7777 -k sync --keep-alive 30 wsgi_app:application`

### Gunicorn async

run `gunicorn --bind :7777 -k gevent --keep-alive 30 wsgi_app:application`

## Testing

- run `python 03_slow_client.py`
- immediately run `python 02_normal_client.py`

## Observations

- for sync variants the normal client has to wait until the slow client finishes
- for async variants, the normal client runs immediately
