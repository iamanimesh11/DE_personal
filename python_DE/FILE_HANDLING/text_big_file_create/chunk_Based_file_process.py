import time
import datetime

def process_file_in_chunks(file_path, chunk_size=1000, search_word="error"):
    d = datetime.datetime.now()
    total_lines = 0
    error_line_numbers = []
    chunk_count = 0  # Counter for the number of chunks processed


    # Open the file for reading
    with open(file_path, 'r') as file:
        while True:
            # Read the file in chunks (1000 lines)
            lines = [file.readline() for i in range(chunk_size)]
            # Break if we reach the end of the file
            if not lines or lines[0] == '':
                break
            # chunk_count += 1  # Increment chunk counter

            # Process each line in the chunk
            for i, line in enumerate(lines):
                if line == '':
                    break  # Stop if end of file reached in the middle of a chunk

                total_lines += 1

                # # Check if the search word (e.g., "error") is in the current line
                # if search_word in line.lower():
                #     error_line_numbers.append(total_lines)

    # Output the results
    # print(f"Total number of chunks processed: {chunk_count}")

    print(f"Total number of lines: {total_lines}")
    print(datetime.datetime.now()-d)

# Call the function with the file path
process_file_in_chunks('big_file', chunk_size=10)
