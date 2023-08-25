"""This script is used to count the number of lines in all the Python files in a project, as well as the size of all the files in the project. The script first sets the directory variable to the current directory using os.path.dirname(__file__), which is the directory in which the script is located. The script then defines the _walk function, which is used to recursively list all the files and directories in the project up to a certain depth specified by the depth parameter.
Next, the script uses the _walk function to create a list of all the files in the project and stores it in the files variable. The script then iterates over this list of files, counts the number of lines in each file, and adds this count to a running total. If a file cannot be opened, it is added to a list of file errors.
After the script has finished counting the lines in all the files, it appends a comment to the end of the script containing the current time and the total line count. The script then gets the current working directory using os.getcwd() and uses the glob module to get a list of all the files in the current directory and its subdirectories. The script then creates a list of tuples containing the file path and size for each file in the project, and sorts this list by file size using the sorted function and a lambda function. Finally, the script prints out the file path, size, and last modified time for each file in the sorted list.
    """

# counting lines in project and distribution and size of files
import os
import time
import glob
import time

size_data = [f"\n{time.time()}"]

# directory = "C:\\Users\\game\\New folder\\user-account-api\\app\\"
# this should be changed to the path of the project
# determine the path
directory = os.path.dirname(__file__)

directory_depth = 100  # How deep you would like to go
extensions_to_consider = [".py"]  # Change to ["all"] to include all extensions
exclude_filenames = ["venv", ".idea", "__pycache__", "cache", "linecount"]
skip_file_error_list = True

this_file_dir = os.path.realpath(__file__)

print("Path to ignore:", this_file_dir)
print("=====================================")


def _walk(path, depth):
    """Recursively list files and directories up to a certain depth"""
    depth -= 1
    with os.scandir(path) as p:
        for entry in p:
            skip_entry = any(entry.path.endswith(fName) for fName in exclude_filenames)
            if skip_entry:
                print("Skipping entry", entry.path)
                continue

            yield entry.path
            if entry.is_dir() and depth > 0:
                yield from _walk(entry.path, depth)


print("Caching entries")
files = list(_walk(directory, directory_depth))
print("=====================================")

print("Counting Lines")
file_err_list = []
line_count = 0
len_files = len(files)
for i, file_dir in enumerate(files):
    if file_dir == this_file_dir:
        print("=[Rejected file directory", file_dir, "]=")
        continue

    if not os.path.isfile(file_dir):
        continue

    skip_File = True
    for ending in extensions_to_consider:
        if file_dir.endswith(ending) or ending == "all":
            skip_File = False

    if not skip_File:
        try:
            with open(file_dir, "r") as file:
                local_count = sum(line != "\n" for line in file)
                print(
                    "({:.1f}%)".format(100 * i / len_files), file_dir, "|", local_count
                )
                line_count += local_count
        except Exception:
            file_err_list.append(file_dir)
            continue
print("=====================================")
print("File Count Errors:", len(file_err_list))
if not skip_file_error_list:
    for file in file_err_list:
        print(file_err_list)

print("=====================================")
print("Total lines |", line_count)

size_data.append(f' {time.strftime("%Y-%m-%d %H:%M:%S")}  {line_count} lines ')

# add time and total line count as a comment to the end of the file
with open(__file__, "a") as myfile:
    myfile.write("\n#  %s  %s lines" % (time.strftime("%Y-%m-%d %H:%M:%S"), line_count))

# Get the current working directory
# and store it in a variable
cwd = os.getcwd()

# Get the list of all files in the
# current working directory
files_list = glob.glob(f"{cwd}/*")

# get list of all files recursively in all subdirectories
files_list = glob.glob(f"{cwd}/**/*", recursive=True)

# Create a list of files
# in directory along with the size
size_of_file = [(f, os.stat(f).st_size) for f in files_list]


# Iterate over list of files along with size
# and print them one by one.
# now we have print the result by
# sorting the size of the file
# so, we have call sorted function
# to sort according to the size of the file

# created a lambda function that help
# us to sort according the size of the file.
def fun(x): return x[1]


# in this case we use its file name.
for f, s in sorted(size_of_file, key=fun):
    print(f"{f} : {round(s / (1024 * 1024), 3)}MB")

# print total size of all files
print(
    f"Total size of all files: {round(sum(s for f, s in size_of_file) / (1024 * 1024), 3)}MB "
)

# add time and total size and file count as a comment to the end of the file
with open(__file__, "a") as myfile:
    myfile.write(
        "\n#  %s  %sMB  %s files"
        % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            round(sum(s for f, s in size_of_file) / (1024 * 1024), 3),
            len(files_list),
        )
    )

size_data.append(
    f"{round(sum(s for f, s in size_of_file) / (1024 * 1024), 3)}MB  {len(files_list)} files"
)

print("File run and saved")

#  2023-07-04 11:18:53  129 lines
#  2023-07-04 11:18:53  0.382MB  19 files

#  2023-07-27 10:01:05  1783 lines
#  2023-07-27 10:01:05  1.808MB  82 files

#  2023-08-14 11:24:33  2391 lines
#  2023-08-14 11:24:33  2.592MB  107 files

#  2023-08-25 08:35:46  2392 lines
#  2023-08-25 08:35:46  2.459MB  100 files