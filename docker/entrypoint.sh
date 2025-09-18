#!/bin/sh

# Aspetta che PostgreSQL sia pronto
while ! nc -z $DB_DEFAULT_HOST $DB_DEFAULT_PORT ; do
    echo "Waiting PostgreSQL ($DB_DEFAULT_HOST:$DB_DEFAULT_PORT)..."
    sleep 3
done

echo "Database available, proceeding with migrations..."

# Esegui migrazioni
python manage.py makemigrations
python manage.py migrate

# Crea superuser solo se non esiste
echo "Checking for superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser(
        username="${DJANGO_SUPERUSER_USERNAME}",
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
    print("Superuser created.")
else:
    print("Superuser already exists, no action needed.")
END

#!/bin/bash
set -e


# Avvio dell'applicazione
echo "|==================================================|"
echo "|   Starting Django server on http://0.0.0.0:8000      |"
echo "|==================================================|"

python manage.py runserver 0.0.0.0:8000 #--noreload