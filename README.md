# mdl-api
Unofficial MyDramaList REST API.

Built using FastAPI and PostgreSQL.

## Installation
Set your environment variables for the Postgres DB: `APP_USER`, `APP_IP`, and `APP_DB`.

Create and initialize the DB with 
```
./scripts/resetdb.sh
```

and then run the web server.

```
uvicorn app.main:app --reload --port 8000
```
