#!/bin/bash

rm -r alembic/versions/*
dropdb mdl
createdb mdl
alembic revision --autogenerate -m "initial db"
alembic upgrade head
