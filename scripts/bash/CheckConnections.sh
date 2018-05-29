#!/bin/bash
# Script to notify if max connection threshold reached
# Exporting Variables
export PGDATABASE='postgres'
export PGPORT=5432
export PGUSER='postgres'     # For greenplum change this value to gpadmin

FILENAME_NOW=$(date +"%Y%m%d%l%M")
LOG_NOW=$(date +"%Y%m%d:%l:%M:%S:%N")
LOGFILE=/tmp/CheckConnections_$FILENAME_NOW.log

# Redirecting output to logfile
exec &> >(while read line; do echo "$(date +'%h %d %H:%M:%S') $line" > "$LOGFILE"; done;)

# Getting total number of connections
TOTAL_CONNECTIONS_NOW=`psql --tuples-only -c 'SELECT count(*) FROM pg_stat_activity'`

# Sending Email if total number of connection are more that 200 using mailx unix utility
if [ $TOTAL_CONNECTIONS_NOW -ge 200 ]
then
    # Getting Total Number of Connections per database
    CONNECTIONS_PER_DATABASE=`psql --tuples-only -c 'SELECT datname AS Database, count(*) AS Connections FROM pg_stat_activity GROUP BY 1;' > /tmp/max_connections_per_database.log`
    echo -e "Hi DBA Team, Total number of connections has reached threshold. \n Total Connections = $TOTAL_CONNECTIONS_NOW \n Please find attachment for details. \n \n Thanks, \n max_connection.sh" | mailx -s 'Too Many connections in Database' -a /tmp/max_connections_per_database.log your@email.id
    echo -e "$ Email sent to your@email.id"
fi
