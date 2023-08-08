# filesystem.py
from file import File
from directory import Directory
import os,shutil,pwd,grp,time,stat
import platform

class FileSystem:
    def __init__(self):
        self.current_directory = Directory(os.getcwd(), None, None, None)
        # self.current_directory = Directory('/', None, None, None)
        os.chdir(self.current_directory.path)
        self.home_directory = self.current_directory  # Initialize 

    
    
    def mkfile():

        print("making")
    
    def resolve_path(self, path):
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
            print(f"Successfully changed directory to {self.current_directory}")
        except Exception as e:
            print(f"Error: {e}")




    

    


    def create_directory(self, directory, recursive=False):
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
   
    # def list_directory(self, path='.', long_format=False, show_hidden=False):
    #     resolved_path = self.resolve_path(path)
    #     for filename in os.listdir(resolved_path):
    #         if filename.startswith('.') and not show_hidden:
    #             continue
    #         if long_format:
    #             self.print_file_info(os.path.join(resolved_path, filename))
    #         else:
    #             print(filename)

    def print_file_info(self, filename):
        info = os.stat(filename)
        file_mode = stat.filemode(info.st_mode)
        n_links = info.st_nlink
        owner = pwd.getpwuid(info.st_uid).pw_name
        group = grp.getgrgid(info.st_gid).gr_name
        size = info.st_size
        mtime = time.ctime(info.st_mtime)
        print(f'{file_mode} {n_links} {owner} {group} {size} {mtime} {filename}')
    
    def move_file(self, source, destination):

        source = self.resolve_path(source)
        destination = self.resolve_path(destination)
        try:
            shutil.move(source, destination)
            print(f'Successfully moved {source} to {destination}')
        except FileNotFoundError:
            print(f'Error: File "{source}" does not exist.')
        except Exception as e:
            print(f'Error: Could not move file "{source}" to "{destination}". {str(e)}')

    def print_working_directory(self):
        print(os.getcwd())
    
    def copy(self, source, destination):
        source = self.resolve_path(source)
        destination = self.resolve_path(destination)
        try:
            if os.path.isdir(source):
                destination = os.path.join(destination, os.path.basename(source))
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            print(f'Successfully copied {source} to {destination}')
        except FileNotFoundError:
            print(f'Error: Source "{source}" does not exist.')
        except Exception as e:
            print(f'Error: Could not copy "{source}" to "{destination}". {str(e)}')

        
    def clear_console(self):
        # Check the platform and use the appropriate clear command
        print('Clearing console')
        if platform.system().lower() == "windows":
            os.system("cls")
        else:
            os.system("clear")

    def change_permission(self, filename, permission):
        filename = self.resolve_path(filename)
        try:
            os.chmod(filename, int(permission, 8))  # Convert permission to an integer base 8
            print(f'Successfully changed permissions of {filename} to {permission}')
        except Exception as e:
            print(f'Error: Could not change permissions of "{filename}". {str(e)}')

    def change_owner_group(self, filename, owner, group):
        filename = self.resolve_path(filename)
        try:
            uid = pwd.getpwnam(owner).pw_uid
            gid = grp.getgrnam(group).gr_gid
            os.chown(filename, uid, gid)
            print(f'Successfully changed owner/group of {filename} to {owner}:{group}')
        except Exception as e:
            print(f'Error: Could not change owner/group of "{filename}". {str(e)}')

    def show_stats(self, filename):
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
        except Exception as e:
            print(f'Error: Could not retrieve statistics for "{filename}". {str(e)}')

    def get_file_type(self, mode):
        if stat.S_ISDIR(mode):
            return 'Directory'
        elif stat.S_ISREG(mode):
            return 'Regular File'
        elif stat.S_ISLNK(mode):
            return 'Symbolic Link'
        # Add more types as needed
        else:
            return 'Unknown'
    
    def edit_file(self, filename):
        filename = self.resolve_path(filename)
        try:
            with open(filename, 'r') as f:
                print(f.read())
            new_content = input("Enter new content for file: ")
            with open(filename, 'w') as f:
                f.write(new_content)
            print(f'Successfully edited {filename}')
        except FileNotFoundError:
            print(f'Error: File "{filename}" does not exist.')
        except PermissionError:
            print(f'Error: Permission denied for editing "{filename}".')
        except Exception as e:
            print(f'Error: Could not edit file "{filename}". {str(e)}')

    def write_to_file(self, message, filename, mode):
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