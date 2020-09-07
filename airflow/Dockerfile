# Here is the build image
FROM python:3.7.0-slim as builder

WORKDIR /root/airflow
COPY requirements.txt .

# Point timezone to Bangkok
ENV TZ=Asia/Bangkok

RUN apt-get update && \
    apt-get install gcc screen sed default-libmysqlclient-dev python-mysqldb -y && \
    apt-get clean && \
    pip install -r requirements.txt

# Set the timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
    
COPY . .

EXPOSE 8080

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]