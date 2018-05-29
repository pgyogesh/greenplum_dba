#!/usr/bin/python
import os
import sys
import smtplib
from gplog import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

logger = get_default_logger()
logger.info('waiting_queries_email.py started')
# Declaring Environment Variables

PGDATABASE='postgres'
PGPORT=5432
PGUSER='gpadmin'
#PGHOST='192.168.2.8'
# Variables for SQL files
WAITING_INFO='/tmp/waiting_info.log'
BRIEF_VIEW_PSQL_STRING='psql -f ~/git/greenplum/lock_monitoring/brief_view.sql'
DESCRIPTION_1= 'psql --tuples-only -c "SELECT \'----------------------------BRIEF_INFO----------------------------\'" > /tmp/waiting_info.log'
BRIEF_VIEW_PSQL_STRING='psql -f ~/git/greenplum/lock_monitoring/brief_view.sql >> /tmp/waiting_info.log'
DESCRIPTION_2= 'psql --tuples-only -c "SELECT \'----------------------------BLOCKERS_INFO-------------------------\'" >> /tmp/waiting_info.log'
BLOCKERS_INFO_PSQL_STRING='psql -f ~/git/greenplum/lock_monitoring/blockers_info.sql >> /tmp/waiting_info.log'
DESCRIPTION_3= 'psql --tuples-only -c "SELECT \'----------------------------WAITERS_INFO--------------------------\'" >> /tmp/waiting_info.log'
WAITERS_INFO_PSQL_STRING='psql -f ~/git/greenplum/lock_monitoring/waiters_info.sql >> /tmp/waiting_info.log'

# Defining function to send email
def sendemail():
    logger.info("Composing email notification")
    to_addr = 'yogeshjadhav96@outlook.com'
    from_addr = 'yogeshjadhav96@gmail.com'
    msg = MIMEMultipart()
    msg['From']=from_addr
    msg['To']=to_addr
    msg['Subject']="Waiting Queries In Greenplum"
    body = "Hi DBA\'s,\n\n There are few queries are waiting in Greenplum.\n Please find the attachments.\n\n Thanks,\n waiting_queries_email.py"
    msg.attach(MIMEText(body, 'plain'))
    filename = 'locking_info.log'
    attachment = open(WAITING_INFO,"rb")
    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login("yogeshjadhav96@gmail.com","Your_Password_here")
    text = msg.as_string()
    logger.info("Sending email from " + from_addr + " to " + to_addr)
    server.sendmail(from_addr,to_addr,text)
    logger.info("Email Sent")
    server.quit()

# Getting True if query is waiting for more than 10 mins
WAITING_PSQL_STRING='psql --tuples-only -c "select distinct waiting from pg_stat_activity where waiting and now() - query_start > \'10 minutes\'::interval"'
IS_WAITING=os.popen(WAITING_PSQL_STRING).read()

# Running PSQL Strings if queries are in waiting state
def get_waiting_info():
    logger.info("Checking if queries are waiting")
    if IS_WAITING.find('t') != -1:
        logger.info("One or more queries are waiting")
        os.popen(DESCRIPTION_1)
        os.popen(BRIEF_VIEW_PSQL_STRING)
        os.popen(DESCRIPTION_2)
        os.popen(BLOCKERS_INFO_PSQL_STRING)
        os.popen(DESCRIPTION_3)
        os.popen(WAITERS_INFO_PSQL_STRING)
        sendemail()
    else:
        logger.info("No queries are waiting. No need to send email")

# Defining main function
def main():
    get_waiting_info()


# Calling main function
if __name__=='__main__':
    main()
    logger.info("waiting_queries.email.py completed successfully")
