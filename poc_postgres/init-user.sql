-- init-user.sql

-- This script runs as the default "postgres" superuser on first init.
-- It uses the env vars that the entrypoint will have already read
-- from your secrets (POSTGRES_USER_FILE, POSTGRES_PASSWORD_FILE, POSTGRES_DB).

CREATE ROLE "${POSTGRES_USER}" WITH LOGIN PASSWORD '${POSTGRES_PASSWORD}';
CREATE DATABASE  "${POSTGRES_DB}" OWNER "${POSTGRES_USER}";
GRANT ALL PRIVILEGES ON DATABASE "${POSTGRES_DB}" TO "${POSTGRES_USER}";