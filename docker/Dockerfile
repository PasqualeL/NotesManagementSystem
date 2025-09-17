FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# installa dipendenze
COPY docker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copia il codice
COPY . /app

#installa connessione db
RUN apt-get update && apt-get install -y netcat-openbsd

# fix permessi e line endings per Windows
RUN chmod +x /app/docker/entrypoint.sh && sed -i 's/\r$//' /app/docker/entrypoint.sh

EXPOSE 8000

CMD ["bash", "-lc", "./docker/entrypoint.sh"]
