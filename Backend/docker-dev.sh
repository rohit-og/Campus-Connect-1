#!/bin/bash
# Docker Development Helper Script

set -e

case "$1" in
  start)
    echo "Starting Docker development environment..."
    docker-compose up -d
    echo "Waiting for services to be healthy..."
    sleep 5
    echo "Services started!"
    echo "API: http://localhost:8000"
    echo "Docs: http://localhost:8000/docs"
    ;;
  stop)
    echo "Stopping Docker development environment..."
    docker-compose down
    ;;
  restart)
    echo "Restarting Docker development environment..."
    docker-compose restart
    ;;
  logs)
    docker-compose logs -f "${2:-backend}"
    ;;
  rebuild)
    echo "Rebuilding backend..."
    docker-compose build backend
    docker-compose up -d backend
    ;;
  shell)
    docker-compose exec backend bash
    ;;
  migrate)
    echo "Running database migrations..."
    docker-compose exec backend alembic upgrade head
    ;;
  clean)
    echo "Stopping and removing all containers, volumes, and networks..."
    read -p "Are you sure? This will delete all data! (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      docker-compose down -v
      echo "Cleanup complete!"
    else
      echo "Cancelled."
    fi
    ;;
  status)
    docker-compose ps
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|logs|rebuild|shell|migrate|clean|status}"
    echo ""
    echo "Commands:"
    echo "  start     - Start all services"
    echo "  stop      - Stop all services"
    echo "  restart   - Restart all services"
    echo "  logs      - View logs (optionally specify service: logs postgres)"
    echo "  rebuild   - Rebuild and restart backend"
    echo "  shell     - Open shell in backend container"
    echo "  migrate   - Run database migrations"
    echo "  clean     - Remove all containers and volumes"
    echo "  status    - Show service status"
    exit 1
    ;;
esac
