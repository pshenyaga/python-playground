#!/bin/sh
gunicorn auth_protected:app --bind localhost:8081 --worker-class aiohttp.worker.GunicornWebWorker --reload
