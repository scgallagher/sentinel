from __future__ import print_function
from logger import log_message

import os

class DirectoryMonitor:

    def __init__(self, input_dir, log_file, debug):

        self.input_dir = input_dir
        self.log_file = log_file
        self.debug = debug
        self.dir_listing = []
        self.first_pass = True

    def scan_dir(self):

        log_message('Scanning ' + self.input_dir, self.log_file, self.debug)

        current_listing = [file for file in os.listdir(self.input_dir)]
        added_files = []
        removed_files = []

        for file in current_listing:

            if file not in self.dir_listing:
                self.dir_listing.append(file)
                added_files.append(file)

        for file in self.dir_listing:

            if file not in current_listing:
                self.dir_listing.remove(file)
                removed_files.append(file)

        log_message('Scan complete.', self.log_file, self.debug)

        return added_files, removed_files
