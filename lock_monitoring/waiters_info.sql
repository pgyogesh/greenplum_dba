SELECT
    l.locktype                    AS  "Waiters locktype",
    d.datname                     AS  "Database",
    l.relation::regclass          AS  "Waiting Table",
    a.usename                     AS  "Waiting user",
    l.pid                         AS  "Waiters pid",
    l.mppsessionid                AS  "Waiters SessionID",
    l.mode                        AS  "Waiters lockmode",
    now()-a.query_start           AS  "Waiting duration",
    SUBSTR(current_query,0,60)    AS  "Waiters Query"
FROM
    pg_locks l,
    pg_stat_activity a,
    pg_database d
WHERE l.pid=a.procpid
AND l.database=d.oid
AND l.granted = 'f'
ORDER BY 3;
