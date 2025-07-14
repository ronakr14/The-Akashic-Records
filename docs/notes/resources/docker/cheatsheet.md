# Cheatsheet

- **Dockerfile Example**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "app.py"]
```

- **CLI Core Commands**:

```bash
docker build -t my-app .
docker run -p 8080:80 my-app
docker exec -it container_id /bin/bash
docker ps
docker stop container_id
docker images
docker rmi image_id
```

- **docker-compose.yml**:

```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    depends_on:
      - db
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret
```

- **Volume Mounting**:

```bash
docker run -v $(pwd):/app my-app
```

- **Multi-Stage Build Snippet**:

```dockerfile
FROM node:18 as builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
```