# marketinsights-dashboard

The dashboard integrates with Redis and Celery. 

To run:

- Ensure redis server is running on the appropriate endpoint

- Navigate to the __server__ folder

    cd ./server

- Start celery

    celery -A app.celery_app worker --loglevel=INFO

- Start the dashboard server

    python app.py
