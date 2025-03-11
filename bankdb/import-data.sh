#!/bin/bash
set -e

echo "Waiting for Oracle DB to start..."
until echo "exit" | sqlplus -S system/123456@//localhost:1521/XEPDB1; do
  echo "Waiting for database connection..."
  sleep 2
done


echo "Creating user..."



sqlplus -S system/123456@//localhost:1521/XE @/docker-entrypoint-initdb.d/init-user.sql

echo "Importing database dump..."
impdp C##BANK_USER/askljnobbDSAi12sSda@//localhost:1521/XE \
    DIRECTORY=DATA_PUMP_DIR \
    DUMPFILE=BANK_USER_DUMP.DMP \
    LOGFILE=import.log \
    REMAP_SCHEMA=ORIGINAL_SCHEMA:C##BANK_USER

echo "Import completed successfully!"

impdp C##BANK_USER/askljnobbDSAi12sSda@//localhost:1521/XE \
    DIRECTORY=DATA_PUMP_DIR \
    DUMPFILE=BANK_USER_DUMP.DMP \
    LOGFILE=import.log \
    REMAP_SCHEMA=ORIGINAL_SCHEMA:C##BANK_USER