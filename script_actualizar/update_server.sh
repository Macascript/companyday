#!/bin/bash

# command=$( cat git_output_test.txt )
command=$( git pull git@github.com:Macascript/companyday.git )

if [[ ${command} == *"changed"* ]] || [[ ${command} == *"insertion"* ]] || [[ ${command} == *"insertion"* ]]; then
    sudo /etc/init.d/apache2 restart
fi
