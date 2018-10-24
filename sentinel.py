from __future__ import print_function

import sys
import smtplib
import os
import time

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

first_pass = True
prev_listing = []

if (len(sys.argv) < 2):
    print('\nUsage: sentinel.py <control file>')
    sys.exit(1)

def parse_control_file():

    control_file_path = sys.argv[1]
    control_file = open(control_file_path, 'r')
    parms = {}

    line = control_file.readline()
    while line:

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

    server = smtplib.SMTP(smtp_host, smtp_port)

    msg_str = message.as_string()

    server.sendmail(from_addr, to_addr, msg_str)

def build_report(added_files, removed_files):

    report = "Report for directory " + input_dir + "\n\n"

    if added_files:
        report += "Added:\n"
        for file in added_files:
            report += "  " + file + "\n"
        report += "\n"

    if removed_files:
        report += "Removed:\n"
        for file in removed_files:
            report += "  " + file + "\n"
        report += "\n"

    report += "Directory Listing:\n"
    for file in prev_listing:
        report += "  " + file + "\n"

    return report

def start_scan():

    while True:

        print('Scanning')

        current_listing = [file for file in os.listdir(input_dir)]
        added_files = []
        removed_files = []

        for file in current_listing:

            if file not in prev_listing:
                prev_listing.append(file)
                added_files.append(file)

        for file in prev_listing:

            if file not in current_listing:
                prev_listing.remove(file)
                removed_files.append(file)

        # print(prev_listing)
        # print(' Added:  ', added_files)
        # print(' Removed:', removed_files)
        report = build_report(added_files, removed_files)
        if first_pass:
            first_pass = False
        else:
            if added_files or removed_files:
                send_email('Sentinel - Directory has been updated', report)

        time.sleep(scan_interval)

parms = parse_control_file()
input_dir = parms.get('input_dir')
from_addr = parms.get('from_addr')
to_addr = parms.get('to_addr')
scan_interval = int(parms.get('scan_interval'))
smtp_host = parms.get('smtp_host')
smtp_port = parms.get('smtp_port')

start_scan()
