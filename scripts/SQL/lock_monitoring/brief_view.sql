SELECT
    kl.pid as blocking_pid,
    ka.usename as blocking_user,
    SUBSTR(ka.current_query,0,20) as blocking_query,
    bl.pid as blocked_pid,
    a.usename as blocked_user,
    SUBSTR(a.current_query,0,20) as blocked_query,
    to_char(age(now(), a.query_start),'HH24h:MIm:SSs') as age
FROM pg_catalog.pg_locks bl
    JOIN pg_catalog.pg_stat_activity a
        ON bl.pid = a.procpid
    JOIN pg_catalog.pg_locks kl
        ON bl.locktype = kl.locktype
        and bl.database is not distinct from kl.database
        and bl.relation is not distinct from kl.relation
        and bl.page is not distinct from kl.page
        and bl.tuple is not distinct from kl.tuple
        --and bl.virtualxid is not distinct from kl.virtualxid
        and bl.transactionid is not distinct from kl.transactionid
        and bl.classid is not distinct from kl.classid
        and bl.objid is not distinct from kl.objid
        and bl.objsubid is not distinct from kl.objsubid
        and bl.pid <> kl.pid
    JOIN pg_catalog.pg_stat_activity ka
        ON kl.pid = ka.procpid
WHERE kl.granted and not bl.granted
ORDER BY a.query_start;
