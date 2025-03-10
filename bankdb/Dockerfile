FROM container-registry.oracle.com/database/express:latest

# Set environment variables
ENV ORACLE_SID=XE
ENV ORACLE_PDB=XEPDB1
ENV ORACLE_PWD=askhboUYOAsbo

# Copy import script and dump file into the container
COPY import-data.sh /opt/oracle/scripts/setup/import-data.sh
RUN chmod +x /opt/oracle/scripts/setup/import-data.sh
COPY BANK_USER_DUMP.DMP /opt/oracle/dump/BANK_USER_DUMP.DMP

