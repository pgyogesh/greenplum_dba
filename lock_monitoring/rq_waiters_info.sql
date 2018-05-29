-- Below SQL Script will display the locks where locktype is Resource Queue
SELECT 
   rsqname                 as "RQname",
   rsqcountlimit           as "RQActivestmt-Limit",
   rsqcountvalue           as "RQActivestmt-Current",
   rsqcostlimit            as "RQCost-Limit",
   rsqcostvalue            as "RQCost-Current",
   rsqmemorylimit::bigint  as "RQMemory-Limit",
   rsqmemoryvalue::bigint  as "RQMemory-Current",
   rsqholders              as "RQHolders",
   rsqwaiters              as "RQWaiters"
FROM gp_toolkit.gp_resqueue_status;
