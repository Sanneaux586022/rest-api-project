# CONTRIBUTING

## How to run Dockerfile locally
```
1. docker network create mynetwork
2. docker run -d --name redis --network mynetwork redis: latest
3. docker run -dp 5000:5000 -w /app -v "$(pwd):/app" --network mynetwork -e REDIS_URL=redis://redis:port IMAGE_NAME\
sh -c "flask run"
```

# DB NEED
```
create your own .env file for your variables
```