screen -dmS "webserver" sh -c 'airflow webserver -p 8080' && \
screen -dmS "scheduler" sh -c 'airflow scheduler'