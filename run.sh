mkdir -p data && \
docker-compose down -v && \
docker-compose up -d && \
docker-compose logs -f