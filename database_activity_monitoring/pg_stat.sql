select * from pg_stat_activity where curren_query not ilike '%IDLE%';
