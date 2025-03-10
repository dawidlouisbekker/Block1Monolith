#!/bin/bash
set -e

# Wait for Oracle to fully start
echo "Oracle DB getting ready..."
until sqlplus -s sys/Oracle123@localhost:1521/XEPDB1 as sysdba <<EOF
exit;
EOF
do
  sleep 5
done

echo "Ready. Importing data..."

# Create BANK_USER user if not exists
sqlplus sys/Oracle123@localhost:1521/XEPDB1 as sysdba <<EOF
CREATE USER BANK_USER IDENTIFIED BY askljnobbDSAi12sSda DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp;
GRANT CONNECT, RESOURCE, DBA TO BANK_USER;
EXIT;
EOF

# Run the Data Pump import
impdp BANK_USER/BankPass@XEPDB1 FULL=Y DIRECTORY=DATA_PUMP_DIR DUMPFILE=BANK_USER_DUMP.DMP LOGFILE=import.log

echo "Import completed successfully!"
