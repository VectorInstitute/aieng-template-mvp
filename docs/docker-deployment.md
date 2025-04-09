# Docker and Deployment

This guide covers Docker configuration and deployment strategies for the MVP template.

## Docker Configuration

The template includes Docker configuration for both development and production environments.

### Docker Files

- `docker-compose.dev.yml`: Development environment configuration
- `docker-compose.yml`: Production environment configuration
- `frontend/Dockerfile.dev`: Frontend development container configuration
- `frontend/Dockerfile`: Frontend production container configuration
- `backend/Dockerfile.dev`: Backend development container configuration
- `backend/Dockerfile`: Backend production container configuration

### Environment Variables

Docker Compose uses environment variables defined in these files:

- `.env.development`: Development environment variables
- `.env.production`: Production environment variables

The template includes `.env.example` as a starting point.

## Development with Docker

Start the development environment:

```bash
docker compose --env-file .env.development -f docker-compose.dev.yml up
```

This will start:
- Frontend development server with hot reloading
- Backend API server with hot reloading
- Any other services defined in `docker-compose.dev.yml`

### Volume Mounts

In development mode, the source code directories are mounted as volumes, allowing for hot reloading:

```yaml
volumes:
  - ./frontend:/app
  - /app/node_modules
```

## Production Deployment

Build and run for production:

```bash
# Set the BUILD_ID environment variable
export BUILD_ID=$(date +%Y%m%d%H%M%S)

# Build the containers
docker compose --env-file .env.production -f docker-compose.yml build

# Run the containers
docker compose --env-file .env.production -f docker-compose.yml up -d
```

Or use the included build script:

```bash
ENVIRONMENT=production ./build.sh
docker compose --env-file .env.production -f docker-compose.yml up -d
```

## Container Registry Deployment

To push images to a container registry:

1. Update the image names in `docker-compose.yml`:

```yaml
image: your-registry.com/your-username/your-project:frontend-${BUILD_ID:-latest}
```

2. Build and push the images:

```bash
# Build the containers
docker compose --env-file .env.production -f docker-compose.yml build

# Push the containers
docker compose --env-file .env.production -f docker-compose.yml push
```

## Customizing Docker Configuration

### Adding New Services

To add a new service, add a new section to the Docker Compose files:

```yaml
new-service:
  build:
    context: ./new-service
    dockerfile: Dockerfile
  environment:
    - VARIABLE=value
  ports:
    - "1234:1234"
  networks:
    - app-network
```

### Customizing Resource Limits

You can add resource limits to your services:

```yaml
services:
  backend:
    # ... other configuration
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Continuous Deployment

The template includes a GitHub Actions workflow in `.github/workflows/ci.yml` that can be extended for continuous deployment:

```yaml
deploy:
  needs: [backend-tests, frontend-tests]
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  steps:
    - uses: actions/checkout@v3
    - name: Deploy to production
      run: |
        # Add your deployment steps here
        echo "Deploying to production..."
```

## Secrets Management

For production deployments, you should use a secrets management solution:

1. Docker Swarm secrets
2. Kubernetes secrets
3. Environment variable encryption

Example using Docker Swarm secrets:

```bash
# Create a secret
echo "my-secret-value" | docker secret create my_secret -

# Reference the secret in docker-compose.yml
secrets:
  my_secret:
    external: true

services:
  backend:
    secrets:
      - my_secret
```

## Health Checks

The template includes health checks for services. You can customize these in the Docker Compose files:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/healthcheck"]
  interval: 10s
  timeout: 5s
  retries: 5
```
