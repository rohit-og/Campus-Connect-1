# Docker Development Environment Setup

This guide will help you set up and run the Campus Connect backend using Docker.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- At least 4GB of available RAM
- Ports 8000, 5432, 27017, 6333, and 6334 available

## Quick Start

1. **Navigate to the Backend directory:**

   ```bash
   cd Backend
   ```

2. **Start all services:**

   ```bash
   docker-compose up -d
   ```

3. **View logs:**

   ```bash
   docker-compose logs -f backend
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Services

The Docker Compose setup includes:

- **backend**: FastAPI application (port 8000)
- **postgres**: PostgreSQL database (port 5432)
- **mongodb**: MongoDB database (port 27017)
- **qdrant**: Qdrant vector database (ports 6333, 6334)

## Environment Variables

### Using .env file (Recommended)

**Option 1: Create a `.env` file (Simplest)**

1. Create a `.env` file in the `Backend` directory:

   ```bash
   # In Backend/.env
   GROQ_API_KEY=your-groq-api-key-here
   QDRANT_API_KEY=your-qdrant-api-key-here
   ```

2. Docker Compose automatically loads variables from `.env` file in the same directory.

**Option 2: Use .env.docker.example**

1. Copy the example file:

   ```bash
   cp .env.docker.example .env
   ```

2. Edit `.env` with your API keys:
   ```bash
   GROQ_API_KEY=your-groq-api-key-here
   QDRANT_API_KEY=your-qdrant-api-key-here
   ```

**Option 3: Set environment variables before running docker-compose**

On Linux/Mac:

```bash
export GROQ_API_KEY=your-groq-api-key-here
docker-compose up -d
```

On Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your-groq-api-key-here"
docker-compose up -d
```

### Or modify docker-compose.yml directly

Edit the `environment` section in `docker-compose.yml` for the backend service (not recommended for secrets).

## Common Commands

### Start services

```bash
docker-compose up -d
```

### Stop services

```bash
docker-compose down
```

### Stop and remove volumes (clean slate)

```bash
docker-compose down -v
```

### Rebuild backend after code changes

```bash
docker-compose build backend
docker-compose up -d backend
```

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Execute commands in backend container

```bash
# Access shell
docker-compose exec backend bash

# Run Python script
docker-compose exec backend python script.py

# Run database migrations
docker-compose exec backend alembic upgrade head
```

### Check service status

```bash
docker-compose ps
```

## Database Access

### PostgreSQL

```bash
# Connect via docker
docker-compose exec postgres psql -U postgres -d campus_connect

# Or use external client
# Host: localhost
# Port: 5432
# User: postgres
# Password: postgres
# Database: campus_connect
```

### MongoDB

```bash
# Connect via docker
docker-compose exec mongodb mongosh campus_connect

# Or use external client
# Host: localhost
# Port: 27017
# Database: campus_connect
```

### Qdrant

- Web UI: http://localhost:6333/dashboard
- API: http://localhost:6333

## Development Workflow

### Hot Reload

The backend service is configured with `API_RELOAD=true` and mounts the code directory as a volume, so code changes will automatically reload the server.

### Database Migrations

Run Alembic migrations inside the container:

```bash
docker-compose exec backend alembic upgrade head
```

### Adding Dependencies

1. Add to `requirements.txt`
2. Rebuild the container:
   ```bash
   docker-compose build backend
   docker-compose up -d backend
   ```

## Troubleshooting

### Port already in use

If a port is already in use, either:

- Stop the conflicting service
- Change the port mapping in `docker-compose.yml`

### Database connection errors

Wait for databases to be healthy:

```bash
docker-compose ps
```

All services should show "healthy" status.

### Backend won't start

Check logs:

```bash
docker-compose logs backend
```

Common issues:

- Missing environment variables
- Database not ready (wait a few seconds)
- Port conflicts

### Reset everything

```bash
# Stop and remove containers, networks, and volumes
docker-compose down -v

# Remove images (optional)
docker-compose down --rmi all

# Start fresh
docker-compose up -d
```

## Production Considerations

⚠️ **This setup is for development only!**

For production:

1. Use proper secrets management
2. Change default passwords
3. Use environment-specific configs
4. Enable SSL/TLS
5. Set up proper backups
6. Use production-grade images
7. Configure resource limits
8. Set up monitoring and logging

## Volumes

Data is persisted in Docker volumes:

- `postgres_data`: PostgreSQL data
- `mongodb_data`: MongoDB data
- `qdrant_data`: Qdrant data
- `uploads_data`: Uploaded files

To backup volumes:

```bash
docker run --rm -v campus_connect_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```
