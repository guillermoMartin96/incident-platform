docker run \
  --name incident-postgres \
  -e POSTGRES_USER=incident \
  -e POSTGRES_PASSWORD=incident \
  -e POSTGRES_DB=incident_platform \
  -p 5432:5432 \
  -d postgres:16
