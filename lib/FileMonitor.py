from __future__ import print_function

import os

class FileMonitor:

    def __init__(self, row_limit=1000):

        self.file_dict = {}
        self.row_limit = row_limit

    def check_for_changes(self, file_path):

        modified = False
        files = self.file_dict.keys()
        current_stat = os.stat(file_path)
        current_mod_time = current_stat.st_mtime

        if file_path in files:
            prev_mod_time = self.file_dict.get(file_path)
            if current_mod_time > prev_mod_time:
                self.file_dict[file_path] = current_mod_time
                modified = True
        else:
            self.file_dict[file_path] = current_mod_time

        return modified

    def check_for_contents(self, file_path):

        stat = os.stat(file_path)

        if stat.st_size > 0:
            contents = self.get_file_contents(file_path)
            return True
        else:
            return False

    def get_file_contents(self, file_path):

        file = open(file_path, 'r')
        line = file.readline()

        row_count = 0
        contents = ''

        while line and row_count < self.row_limit:

            contents += line
            line = file.readline()

        file.close()

        return contents
