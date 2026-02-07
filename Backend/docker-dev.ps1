# Docker Development Helper Script for PowerShell

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Usage: .\docker-dev.ps1 {start|stop|restart|logs|rebuild|shell|migrate|clean|status}" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  start     - Start all services"
    Write-Host "  stop      - Stop all services"
    Write-Host "  restart   - Restart all services"
    Write-Host "  logs      - View logs (optionally specify service: logs postgres)"
    Write-Host "  rebuild   - Rebuild and restart backend"
    Write-Host "  shell     - Open shell in backend container"
    Write-Host "  migrate   - Run database migrations"
    Write-Host "  clean     - Remove all containers and volumes"
    Write-Host "  status    - Show service status"
}

switch ($Command.ToLower()) {
    "start" {
        Write-Host "Starting Docker development environment..." -ForegroundColor Green
        docker-compose up -d
        Write-Host "Waiting for services to be healthy..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        Write-Host "Services started!" -ForegroundColor Green
        Write-Host "API: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    "stop" {
        Write-Host "Stopping Docker development environment..." -ForegroundColor Yellow
        docker-compose down
    }
    "restart" {
        Write-Host "Restarting Docker development environment..." -ForegroundColor Yellow
        docker-compose restart
    }
    "logs" {
        $service = if ($args.Count -gt 0) { $args[0] } else { "backend" }
        docker-compose logs -f $service
    }
    "rebuild" {
        Write-Host "Rebuilding backend..." -ForegroundColor Yellow
        docker-compose build backend
        docker-compose up -d backend
    }
    "shell" {
        docker-compose exec backend bash
    }
    "migrate" {
        Write-Host "Running database migrations..." -ForegroundColor Yellow
        docker-compose exec backend alembic upgrade head
    }
    "clean" {
        Write-Host "Stopping and removing all containers, volumes, and networks..." -ForegroundColor Red
        $confirmation = Read-Host "Are you sure? This will delete all data! (y/N)"
        if ($confirmation -eq 'y' -or $confirmation -eq 'Y') {
            docker-compose down -v
            Write-Host "Cleanup complete!" -ForegroundColor Green
        } else {
            Write-Host "Cancelled." -ForegroundColor Yellow
        }
    }
    "status" {
        docker-compose ps
    }
    default {
        Show-Help
    }
}
