# To prevent "mbind: Operation not permitted", you need to add "--cap-add=sys_nice"
(docker stop airflow-mysql || :) && (docker rm airflow-mysql || :)
docker run -d \
-e MYSQL_ROOT_PASSWORD=root \
-e TZ='Asia/Bangkok' \
-p 3306:3306 \
-v $(pwd)/data:/var/lib/mysql \
--name airflow-mysql \
--cap-add=sys_nice \
--restart=always \
mysql:8.0.20