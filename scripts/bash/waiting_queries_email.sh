#!\bin\bash

# Assigning required variables
WAITING_INFO='/tmp/waiting_info.log'
BRIEF_VIEW_PSQL_STRING=`psql -f ~/git/greenplum/lock_monitoring/brief_view.sql > $WAITING_INFO`
BLOCKERS_INFO_PSQL_STRING=`psql -f ~/git/greenplum/lock_monitoring/blockers_info.sql >> $WAITING_INFO`
WAITERS_INFO_PSQL_STRING=`psql -f ~/git/greenplum/lock_monitoring/waiters_info.sql >> $WAITING_INFO`

# Check if queries are in waiting state
CHECK_IF_WAITING=`psql --tuples-only -c "SELECT DISTINCT waiting FROM pg_stat_activity WHERE now() - query_start > 001000::abstime::timestamp AND waiting"`
if [ -n $CHECK_IF_WAITING ]
then
    $BRIEF_VIEW_PSQL_STRING
    $BLOCKERS_INFO_PSQL_STRING
    $WAITERS_INFO_PSQL_STRING
    echo "Hi DBA Team,\n There are few queries are waiting in Greenplum.\n Please find attachments.\n\n Thanks,\n waiting_queries_email.sh" | mailx -a $WAITING_INFO -s "Waiting Queries In Greenplum" your@email.here
fi
