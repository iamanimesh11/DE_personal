import os
def create_large_file(filename,size_in_mb):
    sizein_Bytes=size_in_mb*1024*1024
    with open(filename,"w") as file:
        data="hello how are you "*1024
        tota_byte_written=0
        while tota_byte_written<sizein_Bytes:
            file.write(data)
            tota_byte_written+=len(data)
    print(f"file '{filename}' create with size {size_in_mb} MB" )


file_name ="big_file"
create_large_file(file_name,5000)