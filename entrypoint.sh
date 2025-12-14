set -e

echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT ..."

until pg_isready \
  -h "$POSTGRES_HOST" \
  -p "$POSTGRES_PORT" \
  -U "$POSTGRES_USER"; do
  sleep 2
done

echo "PostgreSQL is ready"

echo "Starting FastAPI server"
exec uvicorn app.api.main:app --host 0.0.0.0 --port 8000