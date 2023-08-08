# main.py
from filesystem import FileSystem
import os
import logging
logging.basicConfig(filename='filesystem.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    fs = FileSystem()
    while True:
        command = input('$ ')
        logging.info(f'Command entered: {command}')
        parts = command.split()
        command_name = parts[0]
        args = parts[1:]
                # Commands that require arguments
        commands_requiring_args = ['mkdir', 'rmdir', 'mkfile', 'rmfile', 'move', 'rename', 'copy', 'chmod', 'chown', 'stat', 'cat']

        if command_name in commands_requiring_args and len(args) == 0:
            print(f'Error: The {command_name} command requires at least one argument.')
            continue

        if command_name == 'mkdir':
            recursive = '-p' in args
            dirs = [arg for arg in args if arg != '-p']
            for directory in dirs:
                fs.create_directory(directory, recursive)
        
        if command_name == 'rmdir':
            if len(parts) < 2:
                print('Error: No directory names provided.')
                return
            recursive = '-p' in parts
            dirs = [part for part in parts[1:] if part != '-p']  # filtering out the '-p'
            for directory in dirs:
                fs.remove_directory(directory, recursive)
        #makking mutliple files
        
        elif command_name == 'mkfile':
            if len(parts) < 2:
                print('Error: No file names provided.')
                return
            for i in range(1, len(parts)):
                fs.create_file(parts[i])
        #removing file         
        elif command_name == 'rmfile':
                if len(parts) < 2:
                    print('Error: No file names provided.')
                    return
                for i in range(1, len(parts)):
                    fs.remove_file(parts[i])
        
        elif command_name == 'ls':
            options = [arg for arg in args if arg.startswith('-')]
            paths = [arg for arg in args if not arg.startswith('-')]

            long_format = '-l' in options or '-la' in options or '-al' in options
            show_hidden = '-a' in options or '-la' in options or '-al' in options

            path = paths[0] if paths else '.'  # Use the first path if there is any, otherwise use '.'

            fs.list_directory(path, long_format, show_hidden)

        elif command_name == 'move':
            if len(parts) < 3:
                print('Error: Not enough arguments provided.')
                return
            fs.move_file(parts[1], parts[2])

        elif command_name == 'rename':
            if len(parts) < 3:
                print('Error: Not enough arguments provided.')
                return
            fs.rename_file(parts[1], parts[2])
        elif command_name == 'pwd':
            fs.print_working_directory()
            
       
        elif command_name == 'copy':
            if len(parts) < 3:
                print('Error: Not enough arguments provided.')
                return
            fs.copy(parts[1], parts[2])
        
        elif command_name == 'pwd':
            fs.print_working_directory()
        
        elif command_name == 'clear':
            fs.clear_console()
        
        # elif command_name == 'cd':
        #     if parts:
        #         fs.change_directory(parts)
        #     else:
        #         home_directory = os.path.expanduser('~')
        #         fs.change_directory(home_directory)
            # fs.change_directory()

        elif command_name == 'cd':
            if len(parts) == 1:
                args = ['']
            else:
                args = parts[1:]
            fs.change_directory(args[0])    

        elif command_name =='exit':
            break
        
        elif command_name == 'chmod':
            if len(parts) < 3:
                print('Error: Not enough arguments provided.')
                return
            filename = parts[1]
            permission = parts[2]
            fs.change_permission(filename, permission)

        elif command_name == 'chown':
            if len(parts) < 3:
                print('Error: Not enough arguments provided.')
                return
            filename = parts[1]
            owner, group = parts[2].split(':')
            fs.change_owner_group(filename, owner, group)

        elif command_name == 'stat':
            if len(parts) < 2:
                print('Error: No file name provided.')
                return
            filename = parts[1]
            fs.show_stats(filename)
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


        else:
            print(f'Unknown command: {command_name}')
        
        # Similar blocks for other commands...

if __name__ == "__main__":
    main()
