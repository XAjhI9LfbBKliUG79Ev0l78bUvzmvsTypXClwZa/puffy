#!/bin/bash

./build.sh && {
    echo "Build succeeded!"
    
    # TODO add choice to run either dev
    # or production mode, etc
    ./your_service_command
} || {
    echo "Build failed. Exiting..."
    exit 1
}

