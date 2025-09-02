#!/bin/sh

# Authenticate to Dataloop using dtlpy with env and token from .env
python scripts/login.py

python -m uvicorn "scripts.app:app" \
        --reload \
        --host="0.0.0.0" \
        --port=5463 \
        --timeout-keep-alive=60 \
        &

cp /tmp/app/nginx.conf /etc/nginx/conf.d
npm install
npm run dev &

nginx -g 'daemon off;'
