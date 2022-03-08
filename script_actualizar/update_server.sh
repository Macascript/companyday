#!/bin/bash



while true
do
    command=$( git pull https://github.com/Macascript/companyday.git )
    if [[ ${command} == *"changed"* ]] || [[ ${command} == *"insertion"* ]] || [[ ${command} == *"insertion"* ]]; then
        sudo /etc/init.d/apache2 restart
    fi
    sleep 1m
    echo "Hecho"
done
