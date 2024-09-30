import os
def create_large_file(filename,size_in_mb):
    sizein_Bytes=size_in_mb*1024*1024
    data = """This is a test log file.
    Everything is running smoothly.
    No issues detected in the system.
    Error occurred in module X.
    System reboot successful.
    Checking the logs for any errors.
    No error found in the recent logs.
    Warning: Disk space is low.
    Error: Unable to connect to the server.
    System back online after error recovery.
    All services are running normally.
    Regular maintenance completed.
    Error occurred while processing the request.
    System logs cleared.
    Monitoring the network for any issues.
    No further errors detected so far.
    Error: Service timeout detected.
    Backup process completed successfully.
    No error logs found after the last reboot.
    Error occurred in the security module.
    System is stable after the error was handled.
    """  # Your desired log text
    with open(filename,"w") as file:
        tota_byte_written=0
        while tota_byte_written<sizein_Bytes:
            file.write(data)
            tota_byte_written+=len(data)
    print(f"file '{filename}' create with size {size_in_mb} MB" )


file_name = "big_file"
create_large_file(file_name,500)


import datetime
def process_large(filename):
    with open(filename,"r")as file:
        d = datetime.datetime.now()
        s=file.readlines()
        print(len(s))
        print(datetime.datetime.now()-d)

process_large("big_file")
