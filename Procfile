web: gunicorn --workers=6 wsgi:scav_app 
queue: celery -A app.ext.fila worker --loglevel=INFO