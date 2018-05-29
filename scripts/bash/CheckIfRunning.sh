#!\bin\bash

PGDATABASE=postgres
PGUSER=postgres
PGPORT=5432

# Check if Database server is running
IS_RUNNING=`psql -A -t -c "SELECT '1'"`
if [ IS_RUNNING != 1 ]
then
    echo 'Database Server is not running' | mailx -s 'DB Status' your@email.id
fi
