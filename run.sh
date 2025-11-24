#!/bin/bash

./build.sh && {
    echo "Build succeeded!"
    
    # TODO add choice to run either dev
    # or production mode, etc
    uv run uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
} || {
    echo "Build failed. Exiting..."
    exit 1
}

