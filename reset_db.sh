#!/bin/bash

# Database reset script for Docker development
# This script helps reset the database when migrations fail

echo "🔧 Database Reset Script"
echo "======================="
echo ""
echo "This script will help you reset your database for development."
echo ""
echo "Choose an option:"
echo "1. Reset database (fresh start)"
echo "2. Fake initial migration (skip 0001_initial)"
echo "3. Show migration status"
echo "4. Run migrations"
echo "5. Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🗑️  Removing old database..."
        docker-compose down -v
        echo "✅ Database removed"
        echo ""
        echo "🚀 Starting fresh..."
        docker-compose up -d
        docker-compose exec -T web python manage.py migrate
        docker-compose exec -T web python manage.py createsuperuser
        echo "✅ Database reset complete!"
        ;;
    2)
        echo ""
        echo "⏭️  Faking initial migration..."
        docker-compose exec -T web python manage.py migrate --fake-initial
        echo "✅ Migrations faked!"
        ;;
    3)
        echo ""
        echo "📊 Migration status:"
        docker-compose exec -T web python manage.py showmigrations
        ;;
    4)
        echo ""
        echo "🔄 Running migrations..."
        docker-compose exec -T web python manage.py migrate
        echo "✅ Migrations complete!"
        ;;
    5)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

