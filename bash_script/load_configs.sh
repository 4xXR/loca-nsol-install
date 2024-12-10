#!/bin/bash

CONFIG_DIR="/home/developer/Documents/configs"

NCS_CLI="ncs_cli -C -u admin"

if [ -z "$CONFIG_DIR" ] || [ -z "$NCS_CLI" ]; then
    echo "CONFIG_DIR or NCS_CLI are not defined"
    exit 1
fi

#Verify that the directory exists and contains .txt files
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Configuration directory does not exist: $CONFIG_DIR"
    exit 1
fi

if [ -z "$(ls -A $CONFIG_DIR/*.txt 2>/dev/null)" ]; then
    echo "No .txt files found in configuration directory: $CONFIG_DIR"
    exit 1
fi

#Iterate over configuration files
for config_file in $CONFIG_DIR/*.txt; do
    echo "Loading configuration from: $config_file"
    $NCS_CLI << EOF
config
load merge $config_file 
commit
exit
EOF
done
