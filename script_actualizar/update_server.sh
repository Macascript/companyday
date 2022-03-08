#!/bin/bash

command=$( git pull )
if [[ ${command} == *"app.py"* ]]; then
    sudo /etc/init.d/apache2 restart
fi
echo "UPDATE SERVER: No hay cambios"
