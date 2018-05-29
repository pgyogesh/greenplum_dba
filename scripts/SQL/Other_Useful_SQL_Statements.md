### Getting the list of member of a role


```SQL
SELECT a.rolname
FROM pg_roles a 
WHERE pg_has_role(a.oid,'your_rolname', 'member');
```

### Getting list of roles and its members

```SQL
SELECT r.rolname,
    ARRAY(SELECT b.rolname
	  FROM pg_catalog.pg_auth_members m
	  JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid)
	  WHERE m.member = r.oid) as memberof
FROM pg_catalog.pg_roles r
WHERE r.rolname !~ '^pg_'
ORDER BY 1;
```

### SQL statement to get uncompressed size of schema

```SQL
SELECT pg_size_pretty(SUM(sotusize)::BIGINT)
FROM gp_toolkit.gp_size_of_table_uncompressed
WHERE sotuschemaname = '<schema_name>';
```

### SQL statement to get top big tables in schema  

```SQL
SELECT 
	sotuschemaname as Schema,
	sotutablename as Table,
	pg_size_pretty(sotusize::BIGINT) as Size
FROM gp_toolkit.gp_size_of_table_uncompressed 
WHERE sotuschemaname ilike '<schema_name>'
ORDER BY sotusize DESC
LIMIT 50;
```

### SQL statement to get the workfiles per query

```SQL
SELECT 
	datname as Database,
	usename as Username,
	sess_id as Session_ID,
	segid as segment,
	SUBSTR(current_query,0,40) as Current_Query,
	pg_size_pretty(size::BIGINT)as Size,
	numfiles
FROM gp_toolkit.gp_workfile_usage_per_query 
WHERE current_query NOT ilike '%<IDLE>%' 
ORDER BY size desc;
```


### Resource Queue for user

```SQL
SELECT * 
	FROM gp_toolkit.gp_resq_role 
	where rrrolname = 'rolename';
```

### find running queries or statements which are Waiting in Resource Queues

```SQL
SELECT
	rolname
	,rsqname
	,pid
	,granted
	,current_query
	,datname
FROM pg_roles, gp_toolkit.gp_resqueue_status
,pg_locks, pg_stat_activity
WHERE pg_roles.rolresqueue=pg_locks.objid
	AND pg_locks.objid=gp_toolkit.gp_resqueue_status.queueid
	AND pg_stat_activity.procpid=pg_locks.pid
	AND pg_stat_activity.usename=pg_roles.rolname;
```
