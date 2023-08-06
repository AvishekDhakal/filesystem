import os
from file import File
from directory import Directory
import platform
import shutil
import os
import stat
import pwd
import grp
import time


class FileSystem:
    def __init__(self):
        self.current_directory = Directory(os.getcwd(), None, None, None)

    def parse_command(self, command):
        print(f'Received command: {command}') 
        parts = command.split()
        command_name = parts[0]
        print(f'Parsed command: {command_name}') 
        
        if command_name == "clear":
            print('Entered clear command')
            self.clear_console()
            return
        
        args = parts[1:]

        # Handle 'mkdir' command
        if command_name == 'mkdir':
            if len(parts) < 2:
                print('Error: No directory names provided.')
                return
            recursive = '-p' in parts
            dirs = [part for part in parts[1:] if part != '-p']  # filtering out the '-p'
            for directory in dirs:
                self.create_directory(directory, recursive)

        # Handle 'rmdir' command
        if command_name == 'rmdir':
            if len(parts) < 2:
                print('Error: No directory names provided.')
                return
            recursive = '-p' in parts
            dirs = [part for part in parts[1:] if part != '-p']  # filtering out the '-p'
            for directory in dirs:
                self.remove_directory(directory, recursive)
        #makking mutliple files
        
        elif command_name == 'mkfile':
            if len(parts) < 2:
                print('Error: No file names provided.')
                return
            for i in range(1, len(parts)):
                self.create_file(parts[i])
        #removing file         
        elif command_name == 'rmfile':
                if len(parts) < 2:
                    print('Error: No file names provided.')
                    return
                for i in range(1, len(parts)):
                    self.remove_file(parts[i])
        elif command_name == "touch":
            self.mkfile()
        
        elif command_name == 'ls':
            long_format = '-l' in parts or '-la' in parts or '-al' in parts
            show_hidden = '-a' in parts or '-la' in parts or '-al' in parts
            self.list_directory(long_format, show_hidden)
            print("ls received")
            if '-l' in args:
                self.current_directory.long_list_contents()
            else:
                self.current_directory.list_contents()

        elif command_name == 'move':
            if len(parts) < 3:
                print('Error: Not enough arguments provided.')
                return
            self.move_file(parts[1], parts[2])

        elif command_name == 'rename':
            if len(parts) < 3:
                print('Error: Not enough arguments provided.')
                return
            self.rename_file(parts[1], parts[2])
        elif command_name == 'pwd':
            self.print_working_directory()
            
        elif command_name == 'copy':
            if len(parts) < 3:
                print('Error: Not enough arguments provided.')
                return
            self.copy_file(parts[1], parts[2])


        else:
            print(f'Unknown command: {command_name}')
        


    def change_directory(self, path):
        if os.path.isdir(path):
            self.current_directory = Directory(path, None, None, None)
        else:
            print(f'No such directory: {path}')

    def make_directory(self, name):
        self.current_directory.create_subdirectory(name, None, None, None)

    def remove_directory(self, name):
        self.current_directory.delete_subdirectory(name)

    # def make_file(self, name):
    #     path = os.path.join(self.current_directory.path, name)
    #     with open(path, 'w') as f:
    #         pass

    def remove_file(self, name):
        path = os.path.join(self.current_directory.path, name)
        if os.path.isfile(path):
            os.remove(path)
        else:
            print(f'No such file: {path}')
    def change_permission(self, permission):
        os.chmod(self.path, int(str(permission), 8))
        self.permission = permission
    
    def create_subdirectory(self, name, owner, group, permission):
        path = os.path.join(self.path, name)
        os.mkdir(path, int(str(permission), 8))
        return Directory(path, owner, group, permission)

    # def list_directory(self):
    #     contents = self.current_directory.list_contents()
    #     for name in contents:
    #         print(name)
    # def parse_command(self, command):
    #     print(f'Received command: {command}') 

    #     parts = command.split()
    #     command_name = parts[0]
    #     args = parts[1:]

    #     if command_name == 'cd':
    #         self.change_directory(*args)
    #     elif command_name == 'mkdir':
    #         self.make_directory(*args)
    #     elif command_name == 'rmdir':
    #         self.remove_directory(*args)
    #     elif command_name == 'mkfile':
    #         self.make_file(*args)
    #     elif command_name == 'rmfile':
    #         self.remove_file(*args)
    #     elif command_name == 'ls':
    #         self.list_directory()
    #     elif command_name == 'chmod':
    #         self.change_permission(*args)
    #     else:
    #         print(f'Unknown command: {command_name}')

    def change_permission(self, path, permission):
        if os.path.isdir(path):
            dir = Directory(path, None, None, None)
            dir.change_permission(permission)
        elif os.path.isfile(path):
            file = File(path, None, None, None)
            file.change_permission(permission)
        else:
            print(f'No such file or directory: {path}')
    
    def clear_console(self):
        # Check the platform and use the appropriate clear command
        print('Clearing console')
        if platform.system().lower() == "windows":
            os.system("cls")
        else:
            os.system("clear")
    def mkfile():
        print("making")


    def create_directory(self, directory, recursive=False):
        try:
            if recursive:
                os.makedirs(directory, exist_ok=True)
            else:
                os.mkdir(directory)
            print(f'Successfully created directory: {directory}')
        except Exception as e:
            print(f'Error: Could not create directory "{directory}". {str(e)}')

    def remove_directory(self, directory, recursive=False):
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
        try:
            with open(filename, 'x') as f:  # 'x' mode creates a new file and opens it for writing
                pass  # We don't need to write anything to the file, so we just pass
            print(f'Successfully created file: {filename}')
        except FileExistsError:
            print(f'Error: File "{filename}" already exists.')
        except Exception as e:
            print(f'Error: Could not create file "{filename}". {str(e)}')


    def remove_file(self, filename):
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
        try:
            shutil.move(source, destination)
            print(f'Successfully moved {source} to {destination}')
        except FileNotFoundError:
            print(f'Error: File "{source}" does not exist.')
        except Exception as e:
            print(f'Error: Could not move file "{source}" to "{destination}". {str(e)}')
    
    def rename_file(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            print(f'Successfully renamed {old_name} to {new_name}')
        except FileNotFoundError:
            print(f'Error: File "{old_name}" does not exist.')
        except Exception as e:
            print(f'Error: Could not rename file "{old_name}" to "{new_name}". {str(e)}')

    def print_working_directory(self):
        print(os.getcwd())
    
    def copy_file(self, source, destination):
        try:
            shutil.copy2(source, destination)
            print(f'Successfully copied {source} to {destination}')
        except FileNotFoundError:
            print(f'Error: File "{source}" does not exist.')
        except Exception as e:
            print(f'Error: Could not copy file "{source}" to "{destination}". {str(e)}')