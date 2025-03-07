#!/usr/bin/python
import sys
import re

def read_file(read_path) -> list:
    try:
        with open(read_path, 'r') as file:
            return file.readlines()

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def write_file(write_path, content):
    try:
        with open(write_path, 'w') as file:
            file.write(''.join(content))

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def find_first_pos(content) -> list:
    for lIndex in range(len(content)):
        line = content[lIndex]
        # Parse gcode line
        parts = line.split(';', 1)

        if len(parts) > 0:
            command = parts[0].strip()
            
            if command:
                stringMatch = re.search ('^G1 X(.*) Y(.*) ', command)
                if stringMatch:
                    # if find the first G1 position (first point to begin printing)
                    # get the value X-Y and return.

                    return [float(stringMatch.group(1)), float(stringMatch.group(2))]


def add_pruge_macro(content):
    # Locate first position of print-head when print start
    firstPoint = find_first_pos(content)
    # Generate purge macro
    prugeMacro = (f'_TRUE_ADAPTIVE_PURGE X={firstPoint[0]} Y={firstPoint[1]}\n')

    # add purge macro after PRINT_START macro
    for idx, line in enumerate(content, 1):
        if '; Adaptive Purge' in line:
            idx = idx
            content.insert(idx, prugeMacro)
            return content


def process_file(input_f):
    content = read_file(input_f)
    modified_content = add_pruge_macro(content)
    write_file(input_f, modified_content)

if __name__ == '__main__':
    # Check if a file was provided as an argument
    if len(sys.argv) < 1:
        print("Usage: drag and drop a file onto this script.")
        sys.exit(1)

    # The file path is the first argument
    file_path = sys.argv[1]
    # Call the main processing function
    process_file(file_path)
