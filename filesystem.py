
from directory import Directory
import os
import shutil
import pwd
import grp
import time
import stat
import platform
import shutil
import tarfile
import fnmatch


class FileSystem:
    # The FileSystem class is a class that represents a file system.
    def __init__(self):
        self.current_directory = Directory(os.getcwd(), None, None, None)
        os.chdir(self.current_directory.path)
        self.home_directory = Directory(
            os.path.expanduser('~'), None, None, None)

    def resolve_path(self, path):
        """
        The function resolves a given path based on the current directory and returns the absolute path.

        :param path: The `path` parameter is a string that represents a file or directory path
        :return: the resolved path based on the given input path.
        """
        if isinstance(self.current_directory, Directory):
            self.current_directory = self.current_directory.path
        if isinstance(path, Directory):
            path = path.path
        if path == '.':
            # Do nothing and return the current directory
            return self.current_directory
        elif path == '..':
            # Go up one directory level
            return os.path.dirname(self.current_directory)
        elif path == '~' or path == '':
            # Expand ~ or an empty string to the user's home directory
            return os.path.expanduser('~')
        else:
            # For other cases, join the current directory with the given path
            return os.path.join(self.current_directory, path)

    def change_directory(self, new_directory):

        print(f"Changing directory: {new_directory}")

        new_directory = self.resolve_path(new_directory)

        try:
            # If new_directory is a Directory object, get its path
            if isinstance(new_directory, Directory):
                new_directory = new_directory.path

            os.chdir(new_directory)
            self.current_directory = new_directory
            print(
                f"Successfully changed directory to {self.current_directory}")
        except Exception as e:
            print(f"Error: {e}")

    def create_directory(self, directory, recursive=False):
        """
        The function creates a directory at the specified path, with an option to create parent
        directories recursively.

        :param directory: The "directory" parameter is the path of the directory that you want to
        create. It can be either a relative or an absolute path
        :param recursive: The "recursive" parameter is a boolean flag that determines whether the
        directory should be created recursively or not, defaults to False (optional)
        """
        directory = self.resolve_path(directory)
        try:
            if recursive:
                os.makedirs(directory, exist_ok=True)
            else:
                os.mkdir(directory)
            print(f'Successfully created directory: {directory}')
        except Exception as e:
            print(f'Error: Could not create directory "{directory}". {str(e)}')

    def remove_directory(self, directory, recursive=False):
        """
        The function removes a directory and its contents if recursive is set to True, otherwise it only
        removes an empty directory.

        :param directory: The "directory" parameter is the path of the directory that you want to
        remove. It can be either a relative or an absolute path
        :param recursive: The "recursive" parameter is a boolean flag that determines whether to remove
        the directory and its contents recursively or not. If set to True, the function will remove the
        directory and all its subdirectories and files. If set to False, the function will only remove
        the directory if it is empty, defaults to False (optional)
        """
        directory = self.resolve_path(directory)
        try:
            if recursive:
                shutil.rmtree(directory)
            else:
                os.rmdir(directory)
            print(f'Successfully removed directory: {directory}')
        except FileNotFoundError:
            print(f'Error: Directory "{directory}" does not exist.')
        except OSError as e:
            # If the directory is not empty, an OSError will be thrown
            print(f'Error: Directory "{directory}" is not empty. {str(e)}')
        except Exception as e:
            print(f'Error: Could not remove directory "{directory}". {str(e)}')

    def create_file(self, filename):
        """
        The function `create_file` creates a new file with the given filename, handling exceptions for
        file already existing or other errors.

        """
        filename = self.resolve_path(filename)
        try:
            with open(filename, 'x') as f:  # 'x' mode creates a new file and opens it for writing
                pass  # We don't need to write anything to the file, so we just pass
            print(f'Successfully created file: {filename}')
        except FileExistsError:
            print(f'Error: File "{filename}" already exists.')
        except Exception as e:
            print(f'Error: Could not create file "{filename}". {str(e)}')

    def remove_file(self, filename):
        """
        The function removes a file specified by the filename, handling different error cases.

        """
        filename = self.resolve_path(filename)
        try:
            os.remove(filename)
            print(f'Successfully removed file: {filename}')
        except FileNotFoundError:
            print(f'Error: File "{filename}" does not exist.')
        except PermissionError:
            print(f'Error: Permission denied for deleting "{filename}".')
        except Exception as e:
            print(f'Error: Could not remove file "{filename}". {str(e)}')

    def list_directory(self, path='.', long_format=False, show_hidden=False):
        """
        The function `list_directory` lists the files and directories in a given path, with options for
        long format and showing hidden files.
        cluded in the listing, defaults to False (optional)
        """
        resolved_path = self.resolve_path(path)
        if os.path.isfile(resolved_path):
            if long_format:
                self.print_file_info(resolved_path)
            else:
                print(os.path.basename(resolved_path))
        else:
            for filename in os.listdir(resolved_path):
                if filename.startswith('.') and not show_hidden:
                    continue
                if long_format:
                    self.print_file_info(os.path.join(resolved_path, filename))
                else:
                    print(filename)

    def print_file_info(self, filename):
        """
        The function `print_file_info` prints information about a file, including its mode, number of
        links, owner, group, size, modification time, and filename.

        """
        info = os.stat(filename)
        file_mode = stat.filemode(info.st_mode)
        n_links = info.st_nlink
        owner = pwd.getpwuid(info.st_uid).pw_name
        group = grp.getgrgid(info.st_gid).gr_name
        size = info.st_size
        mtime = time.ctime(info.st_mtime)
        print(f'{file_mode} {n_links} {owner} {group} {size} {mtime} {filename}')

    def move_file(self, source, destination):
        """
        The function `move_file` moves a file from a source location to a destination location, handling
        exceptions for file not found and general errors.

        """

        source = self.resolve_path(source)
        destination = self.resolve_path(destination)
        try:
            shutil.move(source, destination)
            print(f'Successfully moved {source} to {destination}')
        except FileNotFoundError:
            print(f'Error: File "{source}" does not exist.')
        except Exception as e:
            print(
                f'Error: Could not move file "{source}" to "{destination}". {str(e)}')

    def print_working_directory(self):
        """
        The function prints the current working directory.
        """
        print(os.getcwd())

    def copy(self, source, destination):
        """
        The `copy` function copies a file or directory from a source path to a destination path,
        handling errors and providing feedback on the operation.

        """
        source = self.resolve_path(source)
        destination = self.resolve_path(destination)
        try:
            if os.path.isdir(source):
                destination = os.path.join(
                    destination, os.path.basename(source))
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            print(f'Successfully copied {source} to {destination}')
        except FileNotFoundError:
            print(f'Error: Source "{source}" does not exist.')
        except Exception as e:
            print(
                f'Error: Could not copy "{source}" to "{destination}". {str(e)}')

    def clear_console(self):
        """
        The function clears the console screen by using the appropriate clear command based on the
        platform.
        """
        # Check the platform and use the appropriate clear command
        print('Clearing console')
        if platform.system().lower() == "windows":
            os.system("cls")
        else:
            os.system("clear")

    def change_permission(self, filename, permission):
        """
        The function `change_permission` changes the permissions of a file specified by `filename` to
        the value specified by `permission`.

        """
        filename = self.resolve_path(filename)
        try:
            # Convert permission to an integer base 8
            os.chmod(filename, int(permission, 8))
            print(
                f'Successfully changed permissions of {filename} to {permission}')
        except Exception as e:
            print(
                f'Error: Could not change permissions of "{filename}". {str(e)}')

    def change_owner_group(self, filename, owner, group):
        """
        The function `change_owner_group` changes the owner and group of a file in Python.

        """
        filename = self.resolve_path(filename)
        try:
            uid = pwd.getpwnam(owner).pw_uid
            gid = grp.getgrnam(group).gr_gid
            os.chown(filename, uid, gid)
            print(
                f'Successfully changed owner/group of {filename} to {owner}:{group}')
        except Exception as e:
            print(
                f'Error: Could not change owner/group of "{filename}". {str(e)}')

    def show_stats(self, filename):
        """
        The function `show_stats` retrieves and displays various statistics of a file specified by the
        `filename` parameter.

        """
        filename = self.resolve_path(filename)
        try:
            stat_info = os.stat(filename)

            print(f'Statistics for {filename}:')
            print(f'File Type: {self.get_file_type(stat_info.st_mode)}')
            print(f'Size: {stat_info.st_size} bytes')
            print(f'Permissions: {oct(stat.S_IMODE(stat_info.st_mode))}')
            print(f'Owner ID: {stat_info.st_uid}')
            print(f'Group ID: {stat_info.st_gid}')
            print(f'Number of Hard Links: {stat_info.st_nlink}')
            print(f'Last Modified: {time.ctime(stat_info.st_mtime)}')
            print(f'Last Accessed: {time.ctime(stat_info.st_atime)}')
            print(f'Last Metadata Change: {time.ctime(stat_info.st_ctime)}')
            return stat_info
        except Exception as e:
            print(
                f'Error: Could not retrieve statistics for "{filename}". {str(e)}')

    def get_file_type(self, mode):
        """
        The function `get_file_type` takes a file mode as input and returns the corresponding file type
        as a string.
        """
        if stat.S_ISDIR(mode):
            return 'Directory'
        elif stat.S_ISREG(mode):
            return 'Regular File'
        elif stat.S_ISLNK(mode):
            return 'Symbolic Link'
        # Add more types as needed
        else:
            return 'Unknown'

    def edit_file(self, filename, new_content=None):
        """
        The `edit_file` function allows for editing the content of a file or printing its content if no
        new content is provided.

        """
        filename = self.resolve_path(filename)
        try:
            if new_content is not None:
                with open(filename, 'w') as f:
                    f.write(new_content)
                print(f'Successfully edited {filename}')
            else:
                with open(filename, 'r') as f:
                    print(f.read())
        except FileNotFoundError:
            print(f'Error: File "{filename}" does not exist.')
        except PermissionError:
            print(f'Error: Permission denied for editing "{filename}".')
        except Exception as e:
            print(f'Error: Could not edit file "{filename}". {str(e)}')

    def write_to_file(self, message, filename, mode):
        """
        The function `write_to_file` writes a message to a file specified by the filename and mode,
        handling various exceptions.

        """
        filename = self.resolve_path(filename)
        try:
            with open(filename, mode) as f:
                f.write(message + '\n')
            print(f'Successfully wrote to {filename}')
        except FileNotFoundError:
            print(f'Error: File "{filename}" does not exist.')
        except PermissionError:
            print(f'Error: Permission denied for writing to "{filename}".')
        except Exception as e:
            print(f'Error: Could not write to file "{filename}". {str(e)}')

    def gzip(self, command_parts):
        """
        The function checks the mode of the gzip command and performs compression or extraction
        accordingly.

        """
        if len(command_parts) < 3:
            print('Error: The gzip command requires at least two arguments.')
            return

        mode = command_parts[1]
        if mode not in ['-c', '-x']:
            print(
                'Error: The gzip command requires a mode: -c for compression or -x for extraction.')
            return

        if mode == '-c':
            self.compress_files(command_parts[2:])
        elif mode == '-x':
            self.extract_file(command_parts[2])

    def edit_file_interactive(self, filename):
        """
        The function `edit_file_interactive` allows the user to interactively edit a file by adding new
        lines of text.

        """

        filename = self.resolve_path(filename)
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()

            print("Enter your text (enter an empty line to save and quit):")
            i = 0
            while i < len(lines):
                print(f"{i+1}: {lines[i]}", end="")
                i += 1
            while True:
                print("Enter new line (leave empty to save and quit):")
                line = input(f"{i+1}: ")
                if line.strip() == "":
                    break
                lines.append(line + '\n')
                i += 1

            with open(filename, 'w') as f:
                f.writelines(lines)
            print(f"Successfully edited {filename}")
        except FileNotFoundError:
            print(f'Error: File "{filename}" does not exist.')
        except PermissionError:
            print(f'Error: Permission denied for editing "{filename}".')
        except Exception as e:
            print(f'Error: Could not edit file "{filename}". {str(e)}')

            with open(filename, 'w') as f:
                f.writelines(lines)
        except FileNotFoundError:
            print(f'Error: File "{filename}" does not exist.')
        except PermissionError:
            print(f'Error: Permission denied for editing "{filename}".')
        except Exception as e:
            print(f'Error: Could not edit file "{filename}". {str(e)}')

    def compress_files(self, file_names):
        """
        The function compresses a list of files into a .tar.gz archive.
        """

        output_file_name = file_names[-1]
        if not output_file_name.endswith('.tar.gz'):
            print('Error: The output file must have a .tar.gz extension.')
            return

        with tarfile.open(output_file_name, 'w:gz') as tar:
            for file_name in file_names[:-1]:
                file_name = self.resolve_path(file_name)
                try:
                    tar.add(file_name)
                    print(f'Successfully added {file_name} to archive')
                except FileNotFoundError:
                    print(f'Error: File "{file_name}" does not exist.')
                except IsADirectoryError:
                    print(f'Error: "{file_name}" is a directory, not a file.')
                except Exception as e:
                    print(
                        f'Error: Could not add file "{file_name}" to archive. {str(e)}')

        print(f'Successfully created archive: {output_file_name}')

    def extract_file(self, file_name):
        """
        The function extracts a .tar.gz file to the same directory as the input file.

        """
        if not file_name.endswith('.tar.gz'):
            print('Error: The input file must have a .tar.gz extension.')
            return

        file_name = self.resolve_path(file_name)
        try:
            with tarfile.open(file_name, 'r:gz') as tar:
                tar.extractall(path=os.path.dirname(file_name))
            print(f'Successfully extracted {file_name}')
        except FileNotFoundError:
            print(f'Error: File "{file_name}" does not exist.')
        except Exception as e:
            print(f'Error: Could not extract file "{file_name}". {str(e)}')

    @staticmethod
    def format_size(size):
        """
        The function "format_size" takes a size in bytes and returns a human-readable format with the
        appropriate unit (B, KB, MB, GB, or TB).
        """

        # formats the size in a human readable format
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit = 0
        while size >= 1024:
            size /= 1024
            unit += 1
        return f'{size:.2f} {units[unit]}'

    def search(self, pattern, path="~"):
        """
        The `search` function searches for files matching a given pattern in a specified directory and
        its subdirectories.
        """

        path = os.path.expanduser('~/Desktop')

        if not os.path.isdir(path):
            print(f'Error: "{path}" is not a directory.')
            return

        matches = []
        for root, dirnames, filenames in os.walk(path, followlinks=True):
            # print(f'Looking in: {root}')  # Debugging line
            for filename in fnmatch.filter(filenames, '*' + pattern + '*'):
                matches.append(os.path.join(root, filename))

        if matches:
            print(f'Found {len(matches)} matches:')
            for match in matches:
                print(match)
            return matches
        else:
            print(f'No files found matching "{pattern}".')

    def disk_usage(self, path='.'):
        """
        The `disk_usage` function calculates the size of a file or directory and returns the size or
        total size respectively.
        """

        path = self.resolve_path(path)
        if os.path.isfile(path):
            size = os.path.getsize(path)
            return size  # Make sure to return the size
        elif os.path.isdir(path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            print(
                f'Total size of directory {path}: {self.format_size(total_size)}')

            return total_size  # Make sure to return the total size
        else:
            print(f'Error: "{path}" is neither a file nor a directory.')
