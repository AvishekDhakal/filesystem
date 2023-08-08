# main.py
from filesystem import FileSystem
import os
import logging
logging.basicConfig(filename='filesystem.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

command_usage = {
        'mkdir': 'mkdir: Creates a new directory.Usage: mkdir [directory_name]',
        'rmdir': 'rmdir: Removes a directory.Usage: rmdir [directory_name]',
        'mkfile': 'mkfile: Creates a new file.Usage: mkfile [file_name]',
        'rmfile': 'rmfile: Removes a file.Usage: rmfile [file_name]',
        'move': 'move: Moves a file or directory.Usage: move [source] [destination]',
        'copy': 'copy: Copies a file or directory.Usage: copy [source] [destination]',
        'chmod': 'chmod: Changes the permissions of a file or directory.Usage: chmod [file_or_directory] [permissions]',
        'chown': 'chown: Changes the owner and group of a file or directory.Usage: chown [file_or_directory] [owner]:[group]',
        'help': 'help: Displays this help message.Usage: help',
        # 'stat': 'stat: Display a more infot '
        'cat': 'cat: Displays the content of a file.\nUsage: cat [file_name]',
        'stat': 'stat: Displays the status of a file or directory.\nUsage: stat [file_or_directory]'
    }


def main():
    fs = FileSystem()
    while True:
        try:
            command = input('$ ')
            logging.info(f'Command entered: {command}')
            parts = command.split()
            command_name = parts[0]
            args = parts[1:]
                    # Commands that require arguments
            if command_name in ['mkdir', 'rmdir', 'mkfile', 'rmfile','stat']:
                if len(args) < 1:
                    print(f'Error: The {command_name} command requires at least one argument.')
                    continue
                else:
                    # Handle these commands...
                    if command_name == 'mkdir':
                        recursive = '-p' in args
                        dirs = [arg for arg in args if arg != '-p']
                        for directory in dirs:
                            fs.create_directory(directory, recursive)
                    
                    elif command_name == 'rmdir':
                        recursive = '-p' in args
                        dirs = [arg for arg in args if arg != '-p']
                        for directory in dirs:
                            fs.remove_directory(directory, recursive)
                    
                    elif command_name == 'mkfile':
                        for i in range(0, len(args)):
                            fs.create_file(args[i])
                    
                    elif command_name == 'rmfile':
                        for i in range(0, len(args)):
                            fs.remove_file(args[i])
                    elif command_name == 'stat':
                        filename = parts[1]
                        fs.show_stats(filename)

                    
            
            elif command_name == 'ls':
                options = [arg for arg in args if arg.startswith('-')]
                paths = [arg for arg in args if not arg.startswith('-')]
                long_format = '-l' in options or '-la' in options or '-al' in options
                show_hidden = '-a' in options or '-la' in options or '-al' in options
                path = paths[0] if paths else '.'  # Use the first path if there is any, otherwise use '.'
                fs.list_directory(path, long_format, show_hidden)

            elif command_name in ['move', 'copy']:
                if len(args) != 2:
                    print(f'Error: The {command_name} command requires exactly two arguments.')
                    continue
                else:
                    source = args[0]
                    destination = args[1]
                    if command_name == 'move':
                        fs.move_file(source, destination)
                    elif command_name == 'copy':
                        fs.copy(source, destination)
            
            elif command_name == 'pwd':
                fs.print_working_directory()
            
            elif command_name == 'clear':
                fs.clear_console()

            elif command_name == 'cd':
                if len(parts) == 1:
                    args = ['']
                else:
                    args = parts[1:]
                fs.change_directory(args[0])    

            elif command_name =='exit':
                break
            
            elif command_name in ['chmod', 'chown']:
                if len(args) < 2:
                    print(f'Error: The {command_name} command requires at least two arguments.')
                    continue
                else:
                    filename = args[0]
                    if command_name == 'chmod':
                        permission = args[1]
                        fs.change_permission(filename, permission)
                    elif command_name == 'chown':
                        owner, group = args[1].split(':')
                        fs.change_owner_group(filename, owner, group)

            
            elif command_name == 'cat':
                filename = parts[1]
                if '>' in parts or '>>' in parts:
                    if '>' in parts:
                        index = parts.index('>')
                        mode = 'w'  # Overwrite file
                    else:
                        index = parts.index('>>')
                        mode = 'a'  # Append to file
                    message = parts[index - 1]
                    output_file = parts[index + 1]
                    fs.write_to_file(message, output_file, mode)
                else:
                    fs.edit_file(filename)
            elif command_name == 'help':
                for usage in command_usage.values():
                    print(usage)
                continue
            else:
                print(f'Unknown command: {command_name}')

        except FileNotFoundError:
            print(f'Error: The specified file or directory does not exist.')
        except IsADirectoryError:
            print(f'Error: The specified path is a directory, but a file was expected.')
        except NotADirectoryError:
            print(f'Error: The specified path is not a directory, but a directory was expected.')
        except PermissionError:
            print(f'Error: You do not have permission to perform this operation.')
        except OSError as e:
            print(f'Error: An OS error occurred: {str(e)}')
        


if __name__ == "__main__":
    main()
