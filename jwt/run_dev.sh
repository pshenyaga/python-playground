#!/bin/sh
gunicorn jwtprotected:app --bind localhost:8080 --worker-class aiohttp.worker.GunicornWebWorker --reload
