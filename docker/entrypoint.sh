#!/bin/sh

# Aspetta che PostgreSQL sia pronto
while ! nc -z $DB_DEFAULT_HOST $DB_DEFAULT_PORT ; do
    echo "In attesa di PostgreSQL ($DB_DEFAULT_HOST:$DB_DEFAULT_PORT)..."
    sleep 3
done

echo "Database disponibile, procedo con le migrazioni..."

# Esegui migrazioni
python manage.py makemigrations
python manage.py migrate

# Crea superuser solo se non esiste
echo "Controllo presenza superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser(
        username="${DJANGO_SUPERUSER_USERNAME}",
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
    print("Superuser creato.")
else:
    print("Superuser già esistente, nessuna azione necessaria.")
END

#!/bin/bash
set -e


# Avvio dell'applicazione
echo "|==================================================|"
echo "|   Avvio server Django su http://0.0.0.0:8000      |"
echo "|==================================================|"

python manage.py runserver 0.0.0.0:8000 #--noreload