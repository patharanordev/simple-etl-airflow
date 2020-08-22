CREATE DATABASE airflow;
USE airflow;
GRANT ALL PRIVILEGES ON airflow.* TO 'root'@'%' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON airflow.* TO 'root'@'localhost' IDENTIFIED BY 'root';