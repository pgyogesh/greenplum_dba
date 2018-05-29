#!/usr/bin/python
import os
import datetime
import sys
import smtplib
from pygresql.pg import DB
import logging

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''|
#             Filename:-                        long_running_queries.py                                                                                 |
#             Version:-                         1.1                                                                                                     |
#             Updated:-                         15th Feb 2018                                                                                           |
#             Updated By:-                      Yogesh Jadhav                                                                                           |
#             Status:-                          Tested                                                                                                  |
#             Author:-                          Yogesh Jadhav                                                                                           |
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''|
# Notes:                                                                                                                                                |
# + This script should run every 1,2,3,5,6,10,15 or 30 to function properly through crontab as it sends first alert anytime it founds long running query|
#   and after that it send email on 30th and 60th minute of an hour.                                                                                    |
#                                                                                                                                                       |
# Version = 1.0                                                                                                                                         |
# + Change ENVIRONMENT to match with environment running script (Line 22)                                                                               |
# + Change MAX_TIME for query duration (In minutes). This is string type. So, Always have this in qoutes                                                |
# + No need change SENDER                                                                                                                               |
# + Change RECIEVERS to add multiple receivers with quoma separator. (Ex: RECEIVERS = 'yogesh.jadhav@yourdomain.com;DBA-Greenplum@yourdomain.com')      |
#                                                                                                                                                       |
# Version = 1.1                                                                                                                                         |
# + Script will send email every 30th minute after 1st alert of same long running query                                                                 |
# + Script will delete lock file at mid night 12:00                                                                                                     |
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,|

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.DEBUG)
logging.info("long_running_queries.py started")

# Declaring Environment Variables

ENVIRONMENT = 'ICDEV/QA'
MAX_TIME = '240'
SENDER = '%s-gpadmin@yourdomain.com' %ENVIRONMENT
RECEIVERS = 'DBA-Greenplum@yourdomain.com'

now = datetime.datetime.now()
minute = int(now.strftime("%M"))
time = int(now.strftime("%H%M"))

# Variables for SQL and Output files
LONG_QUERY_PID="SELECT procpid FROM pg_stat_activity WHERE age(clock_timestamp(),query_start) > interval " + "'%s minutes'" %MAX_TIME + " AND current_query NOT ilike '%IDLE%' LIMIT 1"
LONG_QUERY_PSQL_STRING="""psql -H -c \"SELECT
                                        datname as Database,
                                        procpid as Process_ID,
                                        sess_id as Session_ID,
                                        usename as Username,
                                        SUBSTR(current_query,0,60) as Current_Query,
                                        now() - query_start as Query_Duration,
                                        now() - backend_start as Session_Duration,
                                        waiting as Is_Waiting FROM pg_stat_activity
                                     WHERE
                                        age(clock_timestamp(),query_start) > interval """ + '\'%s minutes\'' %MAX_TIME + """ AND
                                        current_query NOT ilike \'%IDLE%\'
                                     ORDER BY 6 desc;\" """
def sendemail():
    sender = SENDER
    receivers = RECEIVERS

    message = """From: """ + SENDER + """
To: """ + RECEIVERS + """
MIME-Version: 1.0
Content-type: text/html
Subject: Long running queries in """ + ENVIRONMENT + """\n"""
    LONG_RUNNING_QUERIES = os.popen(LONG_QUERY_PSQL_STRING).read()
    message = message + LONG_RUNNING_QUERIES
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
        logging.info("Successfully sent email")
    except SMTPException:
        logging.error("Unable to send email")


logging.info("Checking if queries are running for long time")
try:
    con = DB()
    get_pid = con.query(LONG_QUERY_PID)
    pid = str(get_pid.getresult()[0][0])
    con.close()
except IndexError:
    logging.info("No queries are running for longer time")
    sys.exit()

logging.info("Long running pid: %s" %pid)
if pid and not os.path.isfile('/tmp/long_running_pid_%s' %pid):
        os.popen(LONG_QUERY_PSQL_STRING)
        sendemail()
        os.mknod('/tmp/long_running_pid_%s' %pid)
        logging.info("Lock file created for pid %s" %pid)
elif pid and os.path.isfile('/tmp/log_running_pid_%s' %pid) and (minute == 30 or minute == 00):
        os.popen(LONG_QUERY_PSQL_STRING)
        sendemail()

if time == 1200:
        for file in os.listdir('/tmp/'):
                if 'long_running_pid' in file:
                        os.remove(file)
                        log.info("Deleted pid lock file %s" %file)
