-- Query to check what is running in the Database
-- Below query will give you following details and ordered by duration of running query.
-- 1. Database Name
-- 2. Process ID
-- 3. Session ID
-- 4. Username
-- 5. Brief statement og running query
-- 6. Duration of running query
-- 7. Duration of session
-- 8. waiting
SELECT
  datname as Database,
  procpid as Process_ID,
  sess_id as Session_ID,
  usename as Username,
  SUBSTR(current_query,0,60) as Current_Query,
  now() - query_start as Query_Duration,
  now() - backend_start as Session_Duration,
  waiting as Is_Waiting
FROM pg_stat_activity 
WHERE current_query NOT ilike '%IDLE%' 
ORDER BY 6 desc;
