#!/bin/bash

# Run collectstatic if it's the first time or if necessary
if [ "$1" = "manage.py" ]; then
    # If manage.py is passed as the command, run it with any arguments
    exec python manage.py "$@"
else
    # Run collectstatic to gather static files
    python manage.py collectstatic --noinput

    # Then run Gunicorn to start the application
    exec gunicorn bs23apiproject.wsgi:application --bind 0.0.0.0:8000
fi
