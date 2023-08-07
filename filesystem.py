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
    
    def resolve_path(self, path):
        if isinstance(path, list):
            path = os.path.join(*path)
        if path.startswith('~'):
            path = path.replace('~', self.home_directory.path, 1)
        elif not path.startswith('/'):
            path = os.path.join(self.current_directory.path, path)

        parts = path.split('/')
        new_parts = []
        for part in parts:
            if part == '..':
                if new_parts:
                    new_parts.pop()  # Go up to the parent directory
            elif part and part != '.':
                new_parts.append(part)  # Ignore empty parts and '.'

        return '/' + '/'.join(new_parts)

    def change_directory(self, path):
        path = self.resolve_path(path)
        try:
            os.chdir(path)
            self.current_directory = path
            print(f'Successfully changed directory to {path}')
        except FileNotFoundError:
            print(f'Error: Directory "{path}" does not exist.')
        except NotADirectoryError:
            print(f'Error: "{path}" is not a directory.')
        except PermissionError:
            print(f'Error: Permission denied to change to directory "{path}".')
        except Exception as e:
            print(f'Error: Could not change directory to "{path}". {str(e)}')
    
    def mkfile():
        print("making")
    

    
    # def resolve_path(self, path):
    #     if not path:
    #         return self.current_directory
    #     elif path == '~' or path.startswith('~/'):
    #         return os.path.expanduser(path)
    #     elif os.path.isabs(path):
    #         return path
    #     else:
    #         return os.path.join(self.current_directory, path)


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



    def list_directory(self, long_format=False, show_hidden=False):

        for filename in os.listdir('.'):
            if filename.startswith('.') and not show_hidden:
                continue
            if long_format:
                self.print_file_info(filename)
            else:
                print(filename)

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
    
    def rename_file(self, old_name, new_name):
        filename = self.resolve_path(filename)
        try:
            os.rename(old_name, new_name)
            print(f'Successfully renamed {old_name} to {new_name}')
        except FileNotFoundError:
            print(f'Error: File "{old_name}" does not exist.')
        except Exception as e:
            print(f'Error: Could not rename file "{old_name}" to "{new_name}". {str(e)}')

    def print_working_directory(self):
        # directory = self.resolve_path(directory)
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