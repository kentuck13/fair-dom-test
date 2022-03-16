docker build -t test .
docker-compose -f docker-compose.yml run web
docker-compose down