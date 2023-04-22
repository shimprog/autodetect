sudo pkill -f gunicorn3

gunicorn3 --workers=3 app:app --daemon
