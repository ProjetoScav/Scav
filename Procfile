web: gunicorn --workers=6 --threads=3 wsgi:scav_app 
queue: celery -A app.ext.fila worker --loglevel=INFO