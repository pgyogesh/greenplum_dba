#!/usr/bin/python
from pygresql.pg import DB
import logging
import os
import smtplib
import sys
import datetime
import time
import optparse
import ConfigParser

now = datetime.datetime.now()
start_timestamp = int(now.strftime("%Y%m%d%H%M%S")) # This timestamp will be comapered with timestamp of database backup

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.DEBUG)

parser = optparse.ArgumentParser()
parser.add_option("-a",
                    dest = "silent",
                    action = "store_true",
                    help = "Run program in non-interactive mode")
parser.add_option("-c", "--config-file",
                    dest = "config_file",
                    action = "store",
                    help = "Specify the configuration file path")
parser.add_option("--ddboost",
                    dest = "ddboost",
                    action = "store_true"
                    help = "Use this option for ddboost backup")
options, args = parser.parse_args()

config = ConfigParser.Configparser()
config.read(options.config_file)

logging.info("Reading the configuration file")
database = config.get("conf", "database")
schama = config.get("conf", "schema")


if not dbname:
    logging.error("Database not specified in config_file... Exiting...")
    sys.exit()
"""
This function will get backup latest timestamp from gpcrondump_history table where it is completed successfully
and has used same backup options. So that we can compare the this timestamp with timestamp of this program start.
if backup key has lower value than program timestamp then we can consider that backup is failed.
"""
def get_backupkey():
    con = DB(dbname=source_db, host=source_host, user=source_user)
    opts = backup_command[11:-13]
    key = con.query("SELECT dump_key FROM gpcrondump_history where options = '%s' AND exit_text = 'COMPLETED' ORDER BY dump_key desc limit 1" %opts)
    row = key.dictresult()
    dump_key = row[0]["dump_key"]
    return int(dump_key)

def get_backup_command():
    schama_cmd = ""
    dd = ""
    if schama:
        for s in schama:
            schama_cmd = schama_cmd + "-s" + schama
    if options.ddboost:
        dd = "--ddboost"
    backup_command = "gpcrondump -x %s %s -h -a %s 2> /dev/null" %(database, schama, dd)
    return backup_command

def log_backup_details():
    logging.info("Database name: %s" %database)
    logging.info("Schema name: %s" %schema)
    if options.ddboost:
        logging.info("DDBOOST: Yes")
    else:
        logging.info("DDBOOST: No")


if __name__ == '__main__':
    log_backup_details()
    if options.silent:
        logging.info("Starting Backup")
        os.popen(get_backup_command())
    else:
        prompt = input("Type 'yes' to continue(Default:No)")
        if prompt == 'yes':
            logging.info("Starting Backup")
            os.popen(get_backup_command())
        else:
