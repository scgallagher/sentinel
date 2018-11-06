from datetime import datetime

def log_message(message, log_file=None, debug=False):

    time_format = "%H:%M:%S"
    timestamp = datetime.now().time()

    line = "[" + timestamp.__format__(time_format) + "] " + message
    if log_file:
        log_file.write(line + "\n")
        if debug:
            print(line)
    else:
        print(line)
