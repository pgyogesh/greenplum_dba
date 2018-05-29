#!/bin/bash
LOG_LOCATION=$MASTER_DATA_DIRECTORY/pg_log
for file in `basename $LOG_LOCATION/gpdb*.csv`
do
    YEAR=`echo ${file:5:4}`
    MONTH=`echo ${file:10:2}`
    if [ -d $LOG_LOCATION/$YEAR/$MONTH ]
    then
        tar czf $LOG_LOCATION/$YEAR/$MONTH/$file.tar.gz $LOG_LOCATION/$FILE
        rm $LOG_LOCATION/$FILE
    else
        mkdir -p $LOG_LOCATION/$YEAR/$MONTH
        tar czf  $LOG_LOCATION/$YEAR/$MONTH/$file.tar.gz $LOG_LOCATION/$FILE
        rm $LOG_LOCATION/$file
    fi
done
