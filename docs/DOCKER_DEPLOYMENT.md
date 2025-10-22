# Docker Deployment Guide

This guide covers containerizing and deploying the Flask chat application using Docker.

---

## Prerequisites

- Docker installed (version 20.10+)
- Docker Compose V2 installed (version 2.0+)
- `.env` file configured with Azure OpenAI credentials
- `experimental_conditions.json` configured with study parameters

**Note:** This guide uses Docker Compose V2 syntax (`docker compose` with a space). If you have the legacy V1 (`docker-compose` with a hyphen), the commands work identically - just replace the space with a hyphen. However, V2 is recommended as V1 is deprecated.

---

## Quick Start

```bash
# 1. Build the image
docker build -t chat-experiment:latest .

# 2. Run the container
docker run -d \
  --name chat-experiment \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/experimental_conditions.json:/app/experimental_conditions.json \
  chat-experiment:latest

# 3. Check it's running
docker ps
curl http://localhost:5000/health

# 4. View logs
docker logs -f chat-experiment

# 5. Stop container
docker stop chat-experiment
docker rm chat-experiment
```

---

## Using Docker Compose (Recommended for Development)

### Start the Application

```bash
# Build and start in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

### Access the Application

```
http://localhost:5000/?participant_id=TEST001&condition=0
```

### Manage Data

```bash
# Export conversations (files saved to host's data/ folder)
docker compose exec chat-app python db_utils.py export-conversations

# View stats
docker compose exec chat-app python db_utils.py stats

# Access container shell
docker compose exec chat-app /bin/bash
```

---

## Production Deployment

### Build Production Image

```bash
# Build with tag
docker build -t your-registry.university.edu/chat-experiment:v1.0 .

# Or use docker-compose
docker-compose build
```

### Run in Production

```bash
docker run -d \
  --name chat-experiment \
  --restart unless-stopped \
  -p 5000:5000 \
  -e MODEL_ENDPOINT=https://... \
  -e MODEL_DEPLOYMENT=gpt-4 \
  -e MODEL_API_VERSION=2024-02-15-preview \
  -e MODEL_SUBSCRIPTION_KEY=your-key \
  -e MODEL_MAX_RETRIES=5 \
  -e MODEL_RETRY_DELAY=2.0 \
  -e FLASK_SECRET_KEY=$(openssl rand -hex 32) \
  -e DATABASE_URL=sqlite:///data/chat_experiment.db \
  -v /var/chat-experiment/data:/app/data \
  -v /var/chat-experiment/logs:/app/logs \
  -v /var/chat-experiment/experimental_conditions.json:/app/experimental_conditions.json \
  chat-experiment:latest
```

### Using Environment File

```bash
# Create production .env file (deployment settings only)
# Model parameters go in experimental_conditions.json

# Then run:
docker run -d \
  --name chat-experiment \
  --restart unless-stopped \
  -p 5000:5000 \
  --env-file .env \
  -v /var/chat-experiment/data:/app/data \
  -v /var/chat-experiment/logs:/app/logs \
  -v /var/chat-experiment/experimental_conditions.json:/app/experimental_conditions.json \
  chat-experiment:latest
```

---

## Volume Management

### Data Persistence

The container uses volumes for:

**Experimental Configuration:**
- Container: `/app/experimental_conditions.json`
- Host: `./experimental_conditions.json`
- Contains: Study metadata and conditions (including model parameters)

**Database:**
- Container: `/app/data`
- Host: `./data` (or `/var/chat-experiment/data` in production)
- Contains: `chat_experiment.db`

**Logs:**
- Container: `/app/logs`
- Host: `./logs` (or `/var/chat-experiment/logs` in production)
- Contains: `access.log`, `error.log`

**Static Images:**
- Container: `/app/app/static/images`
- Host: `./app/static/images`
- Contains: `chip.png`, `brain.png`

### Backup Data

```bash
# Backup database
docker cp chat-experiment:/app/data/chat_experiment.db ./backup_$(date +%Y%m%d).db

# Or if using volumes
cp data/chat_experiment.db backups/chat_experiment_$(date +%Y%m%d).db

# Backup experimental configuration
cp experimental_conditions.json backups/experimental_conditions_$(date +%Y%m%d).json
```

---

## Environment Variables

### Required (Deployment Settings)

```env
# Azure OpenAI API Configuration
MODEL_ENDPOINT=https://your-resource.openai.azure.com/
MODEL_DEPLOYMENT=gpt-4
MODEL_API_VERSION=2024-02-15-preview
MODEL_SUBSCRIPTION_KEY=your-api-key

# Retry Configuration
MODEL_MAX_RETRIES=5
MODEL_RETRY_DELAY=2.0

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///data/chat_experiment.db
```

### Study-Specific Configuration (NOT in .env)

Model parameters are now configured in `experimental_conditions.json`:

```json
{
  "study_metadata": {
    "default_model_params": {
      "temperature": 1.0,
      "max_completion_tokens": 2500
    }
  }
}
```

**Why the separation?**
- `.env` = Deployment configuration (same across studies)
- `experimental_conditions.json` = Study configuration (different per study)
- This makes studies more portable and self-contained

---

## Health Checks

The container includes health check endpoints:

```bash
# Health check (basic liveness)
curl http://localhost:5000/health

# Readiness check (database connection)
curl http://localhost:5000/ready
```

Docker will automatically restart unhealthy containers.

---

## Deployment with Nginx Reverse Proxy

### docker-compose with Nginx

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  chat-app:
    build: .
    restart: unless-stopped
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./experimental_conditions.json:/app/experimental_conditions.json:ro
    environment:
      - MODEL_ENDPOINT=${MODEL_ENDPOINT}
      - MODEL_DEPLOYMENT=${MODEL_DEPLOYMENT}
      - MODEL_API_VERSION=${MODEL_API_VERSION}
      - MODEL_SUBSCRIPTION_KEY=${MODEL_SUBSCRIPTION_KEY}
      - MODEL_MAX_RETRIES=${MODEL_MAX_RETRIES}
      - MODEL_RETRY_DELAY=${MODEL_RETRY_DELAY}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
    expose:
      - "5000"
    networks:
      - chat-network

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - chat-app
    networks:
      - chat-network

networks:
  chat-network:
    driver: bridge
```

### Nginx Configuration

Create `nginx.conf`:

```nginx
upstream chat-app {
    server chat-app:5000;
}

server {
    listen 80;
    server_name your-domain.university.edu;

    location / {
        proxy_pass http://chat-app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for LLM responses
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    location /static {
        proxy_pass http://chat-app/static;
        expires 30d;
    }
}
```

Run:
```bash
docker compose -f docker-compose.prod.yml up -d
```

---

## Building for Different Platforms

### For University Registry

```bash
# Build
docker build -t registry.university.edu/chat-experiment:v1.0 .

# Push to registry
docker push registry.university.edu/chat-experiment:v1.0
```

### Multi-platform Build

```bash
# Build for both amd64 and arm64
docker buildx build --platform linux/amd64,linux/arm64 \
  -t chat-experiment:latest .
```

---

## Kubernetes Deployment (Optional)

If deploying to Kubernetes, create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-experiment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: chat-experiment
  template:
    metadata:
      labels:
        app: chat-experiment
    spec:
      containers:
      - name: chat-experiment
        image: registry.university.edu/chat-experiment:v1.0
        ports:
        - containerPort: 5000
        env:
        - name: MODEL_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: chat-secrets
              key: model-endpoint
        - name: MODEL_SUBSCRIPTION_KEY
          valueFrom:
            secretKeyRef:
              name: chat-secrets
              key: api-key
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: config
          mountPath: /app/experimental_conditions.json
          subPath: experimental_conditions.json
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: chat-data-pvc
      - name: config
        configMap:
          name: experimental-conditions
---
apiVersion: v1
kind: Service
metadata:
  name: chat-experiment
spec:
  selector:
    app: chat-experiment
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs chat-experiment

# Run interactively to debug
docker run -it --rm --env-file .env \
  -v $(pwd)/experimental_conditions.json:/app/experimental_conditions.json \
  chat-experiment:latest /bin/bash

# Inside container, test manually:
python wsgi.py
```

### Missing experimental_conditions.json

```bash
# Error: FileNotFoundError: experimental_conditions.json
# Solution: Mount the file as a volume

docker run -v $(pwd)/experimental_conditions.json:/app/experimental_conditions.json ...
```

### Permission errors

```bash
# Fix data directory permissions
chmod -R 777 data logs

# Or run container as specific user
docker run --user $(id -u):$(id -g) ...
```

### Database locked errors

SQLite doesn't handle concurrent writes well. If you get database locked errors:
- Use only 1 worker: `--workers 1`
- Or switch to PostgreSQL for multi-replica deployments

### Model parameter changes not taking effect

```bash
# Model parameters are in experimental_conditions.json, not .env
# After editing experimental_conditions.json:

# If using volume mount, just restart:
docker compose restart

# If config baked into image, rebuild:
docker compose up -d --build
```

### Image too large

```bash
# Check image size
docker images chat-experiment

# Use multi-stage build or alpine base for smaller size
```

### Can't access from outside

```bash
# Check port binding
docker ps

# Test from inside container
docker exec chat-experiment curl http://localhost:5000/health

# Check firewall
sudo ufw status
```

---

## Development Workflow

### Local Development with Hot Reload

For development, use volume mounts for code:

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  chat-app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./app:/app/app
      - ./bot.py:/app/bot.py
      - ./experimental_conditions.json:/app/experimental_conditions.json
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=True
    command: python -m flask run --host 0.0.0.0
```

Run:
```bash
docker compose -f docker-compose.dev.yml up
```

Code changes are reflected immediately!

---

## Cheat Sheet

```bash
# Build
docker build -t chat-experiment .

# Run with .env
docker compose up -d

# Logs
docker compose logs -f

# Shell access
docker compose exec chat-app /bin/bash

# Export data (saves to host's data/ folder)
docker compose exec chat-app python db_utils.py export-conversations

# Restart
docker compose restart

# Stop and remove
docker compose down

# Rebuild after code changes
docker compose up -d --build

# View current model parameters
docker compose exec chat-app python -c "import json; print(json.load(open('experimental_conditions.json'))['study_metadata']['default_model_params'])"
```

---

## Production Checklist

- [ ] `.env` file configured with production credentials (deployment settings only)
- [ ] `experimental_conditions.json` configured with study parameters
- [ ] `FLASK_SECRET_KEY` is a secure random value
- [ ] Model parameters set in `experimental_conditions.json` (not .env)
- [ ] Data volume configured for persistence
- [ ] Config file mounted as volume
- [ ] Logs volume configured
- [ ] Health checks working
- [ ] Nginx reverse proxy configured (if using)
- [ ] HTTPS certificates installed
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Image pushed to registry
- [ ] Resource limits set (CPU, memory)

---

## Configuration Management

### Updating Model Parameters

```bash
# Edit experimental_conditions.json on host
vim experimental_conditions.json

# If using volume mount, just restart:
docker compose restart

# Verify new parameters loaded:
docker compose exec chat-app python -c "from bot import load_experiment_config; print(load_experiment_config(0)['temperature'])"
```

### Updating Study Configuration

All study-specific configuration is in `experimental_conditions.json`:
- Model parameters (temperature, max_tokens)
- Identity protection templates
- Experimental conditions
- System prompts

Mount this file as a volume for easy updates without rebuilding images.

---

## Next Steps

Once containerized:
1. Test locally with `docker compose up`
2. Push image to university registry
3. Deploy to server/Kubernetes
4. Configure Nginx/ingress
5. Set up monitoring
6. Test Qualtrics integration

Your application is now containerized and ready for modern deployment! 🐳