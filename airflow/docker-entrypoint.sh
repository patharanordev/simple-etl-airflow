# screen -dmS "scheduler" sh -c 'airflow scheduler' && \
export AIRFLOW_HOME=/root/airflow && \
airflow initdb && \
sed -i 's/localhost/0.0.0.0/g' $AIRFLOW_HOME/airflow.cfg && \
sed -i 's/smtp_host = 0.0.0.0/smtp_host = mailhog/g' $AIRFLOW_HOME/airflow.cfg && \
sed -i 's/smtp_starttls = True/smtp_starttls = False/g' $AIRFLOW_HOME/airflow.cfg && \
sed -i 's/smtp_port = 25/smtp_port = 1025/g' $AIRFLOW_HOME/airflow.cfg && \
sed -i 's/smtp_mail_from = airflow@example.com/smtp_mail_from = airflow@mailhog.local/g' $AIRFLOW_HOME/airflow.cfg && \
sed -i 's/@0.0.0.0:3306\/airflow/@airflow-mysql:3306\/airflow/g' $AIRFLOW_HOME/airflow.cfg && \
screen -dmS "webserver" sh -c 'airflow webserver -p 8080' && \
airflow scheduler