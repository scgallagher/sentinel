class FileMonitor:

    def __init__(self, scan_dir):

        self.dir_listing = []
        self.first_pass = True

    def scan_dir(self):

        print('Scanning', self.scan_dir)

        current_listing = [file for file in os.listdir(self.scan_dir)]
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

        return added_files, removed_files
