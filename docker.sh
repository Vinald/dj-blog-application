#!/bin/bash

# Django Blog Application - Docker Management Script

case "$1" in
  up)
    echo "Starting Docker containers..."
    docker-compose up -d
    echo "Running migrations..."
    docker-compose exec web python manage.py migrate
    echo "Creating superuser..."
    docker-compose exec web python manage.py createsuperuser
    echo "Application running at http://localhost:8000"
    ;;
  down)
    echo "Stopping Docker containers..."
    docker-compose down
    ;;
  logs)
    docker-compose logs -f
    ;;
  test)
    echo "Running tests..."
    docker-compose exec web pytest
    ;;
  shell)
    docker-compose exec web python manage.py shell
    ;;
  bash)
    docker-compose exec web bash
    ;;
  migrate)
    docker-compose exec web python manage.py migrate
    ;;
  makemigrations)
    docker-compose exec web python manage.py makemigrations
    ;;
  static)
    docker-compose exec web python manage.py collectstatic --noinput
    ;;
  *)
    echo "Usage: $0 {up|down|logs|test|shell|bash|migrate|makemigrations|static}"
    exit 1
    ;;
esac

