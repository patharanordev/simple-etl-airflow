# Here is the build image
FROM python:3.7.0-slim as builder

WORKDIR /root/airflow
COPY requirements.txt .

RUN apt-get update && \
    apt-get install gcc screen sed default-libmysqlclient-dev python-mysqldb -y && \
    apt-get clean && \
    pip install -r requirements.txt
    
COPY . .

# # Airflow config
# RUN airflow initdb && \
#     sed -i 's/localhost/0.0.0.0/g' /root/airflow/airflow.cfg

# # Mailhog config
# # 's/smtp_ssl = False/smtp_ssl = False/g'
# # 's/smtp_user =/smtp_user =/g'
# # 's/smtp_password =/smtp_password =/g'
# RUN sed -i 's/smtp_host = 0.0.0.0/smtp_host = mailhog/g' /root/airflow/airflow.cfg && \
#     sed -i 's/smtp_starttls = True/smtp_starttls = False/g' /root/airflow/airflow.cfg && \
#     sed -i 's/smtp_port = 25/smtp_port = 1025/g' /root/airflow/airflow.cfg && \
#     sed -i 's/smtp_mail_from = airflow@example.com/smtp_mail_from = airflow@mailhog.local/g' /root/airflow/airflow.cfg

# # MySQL config
# RUN sed -i 's/@0.0.0.0:3306\/airflow/@airflow-mysql:3306\/airflow/g' /root/airflow/airflow.cfg

EXPOSE 8080

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]