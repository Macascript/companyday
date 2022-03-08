#!/bin/bash



while true
do
    command=$( git pull )
    if [[ ${command} == *"app.py"* ]]; then
        sudo /etc/init.d/apache2 restart
    fi
    sleep 1m
    echo "Hecho"
done
