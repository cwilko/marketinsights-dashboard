# marketinsights-dashboard

The dashboard integrates with Redis and Celery. 

To run:

- Ensure redis server is running on the appropriate endpoint

- Start celery

    celery -A app.celery_app worker --loglevel=INFO

- Start the dashboard server

    cd ./server
    python app.py
