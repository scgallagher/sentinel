from __future__ import print_function

import sys
import smtplib
import os
import time
import re
import socket

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from lib.DirectoryMonitor import DirectoryMonitor
from lib.FileMonitor import FileMonitor
from lib.logger import log_message

from string import replace

if (len(sys.argv) < 2):
    print('\nUsage: sentinel.py <control file>')
    sys.exit(1)

def parse_control_file():

    control_file_path = sys.argv[1]
    control_file = open(control_file_path, 'r')
    parms = {}

    line = control_file.readline()
    while line:

        if line != '\n' and line[0] != '#':

            key, value = line.split('=')
            parms[key] = value.strip()

        line = control_file.readline()

    return parms

def send_email(subject, body):

    message = MIMEMultipart()
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))
    msg_str = message.as_string()

    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=60)
        server.sendmail(from_addr, to_addr, msg_str)
        server.quit()
    except smtplib.SMTPServerDisconnected:
        log_message('WARNING: SMTP socket timeout - email not sent', log_file, debug)

def build_report(changes):

    report = "Report for directory " + input_dir + "\n\n"

    for change in changes:

        report += change.get('file') + '\n'
        report += change.get('contents') + '\n\n'

    return report

def notify(changes):

    report = build_report(changes)
    log_message('Sending email report', log_file, debug)
    send_email('Sentinel - Files have been modified', report)
    log_message('Email report sent to ' + to_addr, log_file, debug)

def monitor_file(file_list):

    fm = FileMonitor()
    previous_changes = []
    changes = []

    while True:

        if verbose:
            log_message('Running scan', log_file, debug)

        for file in file_list:

            filepath = input_dir + file
            modified = fm.check_for_contents(filepath)

            if modified:
                contents = fm.get_file_contents(filepath)
                changes.append({'file': file, 'contents': contents})
                if verbose:
                    log_message("File " + file + " has been modified", log_file, debug)
            elif verbose:
                log_message("No changes to " + file, log_file, debug)

        notifications = [change for change in changes if change.get('file') not in
            [p.get('file') for p in previous_changes]]
        if notifications:
            notify(notifications)
            previous_changes += notifications
        else:
            log_message('No changes', log_file, debug)
        changes = []

        time.sleep(scan_interval)

def monitor_file_regex():

    files = [file for file in os.listdir(input_dir)]
    matches = []

    for file in files:

        match = re.search(regex, file)
        if match:
            matches.append(file)

    if not matches:
        log_message('WARNING: No regex matches', log_file, debug)

    monitor_file(matches)

parms = parse_control_file()

input_dir = parms.get('input_dir')
input_dir = replace(input_dir, '\\', '/')
if input_dir[len(input_dir) - 1] <> '/':
    input_dir += '/'

input_files = parms.get('input_files')
if input_files:
    input_files = input_files.split(',')

from_addr = parms.get('from_addr')
to_addr = parms.get('to_addr')
scan_interval = int(parms.get('scan_interval'))
smtp_host = parms.get('smtp_host')
smtp_port = parms.get('smtp_port')
log_dir = parms.get('log_dir')
regex = parms.get('regex')
verbose = parms.get('verbose')
debug = parms.get('debug')

log_file_path = log_dir + 'log.txt'
log_file = open(log_file_path, 'a')

log_message('Sentinel service started', log_file, debug)

if input_files:
    monitor_file(input_files)
elif regex:
    monitor_file_regex()
else:
    log_message('FATAL ERROR: Nothing to monitor', log_file, debug)
    sys.exit(2)
