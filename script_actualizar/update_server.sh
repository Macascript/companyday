#!/bin/bash

# command=$( cat git_output_test.txt )
command=$( git pull https://github.com/Macascript/companyday.git )

while true
do
    if [[ ${command} == *"changed"* ]] || [[ ${command} == *"insertion"* ]] || [[ ${command} == *"insertion"* ]]; then
        sudo /etc/init.d/apache2 restart
    fi
    sleep 1m
    echo "Hecho"
done
