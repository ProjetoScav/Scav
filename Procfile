web: gunicorn --workers=6 --threads=3 wsgi:scav_app && celery -A app.ext.fila worker --loglevel=INFO