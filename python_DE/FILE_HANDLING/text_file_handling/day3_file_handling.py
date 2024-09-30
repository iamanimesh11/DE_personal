def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        for line_num, (line1, line2) in enumerate(zip(f1, f2), start=1):
            if line1 != line2:
                print(f"Difference in line {line_num}:")
                print(f"File1: {line1.strip()}")
                print(f"File2: {line2.strip()}")

    # Check if file sizes differ, in case one file has more lines than the other
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines_f1 = f1.readlines()
        lines_f2 = f2.readlines()

        if len(lines_f1) > len(lines_f2):
            print(f"File1 has extra lines starting from line {len(lines_f2) + 1}")
        elif len(lines_f2) > len(lines_f1):
            print(f"File2 has extra lines starting from line {len(lines_f1) + 1}")

# Example usage:
file1 = "1.txt"
file2 = "2.txt"
# compare_files(file1, file2)

def server_log(filename):
    with open(filename,"r") as file:
        s= file.readlines()
        count={}
        for i in s:
            print(i.split()[2])
            if i.split()[2] in count:
                count[i.split()[2]]+=1
            else:
                count[i.split()[2]] = 1

        print(count)


# server_log("server.log")
