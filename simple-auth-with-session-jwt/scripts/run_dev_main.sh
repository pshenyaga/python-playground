#!/bin/sh
gunicorn auth_main:app --bind localhost:8080 --worker-class aiohttp.worker.GunicornWebWorker --reload
