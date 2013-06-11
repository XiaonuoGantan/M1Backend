#!/bin/bash
if [ "$1" == "dev" ]; then
    cat fuzzitusbackend/settings_basic.py fuzzitusbackend/settings_dev.py > fuzzitusbackend/settings.py
elif [ "$1" == "prod" ]; then
    cat fuzzitusbackend/settings_basic.py fuzzitusbackend/settings_prod.py > fuzzitusbackend/settings.py
else
    echo "provide an arugment of either 'dev' or 'prod'"
fi
