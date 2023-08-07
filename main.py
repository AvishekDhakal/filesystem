# main.py
from filesystem import FileSystem
import os
def main():
    fs = FileSystem()
    while True:
        command = input('$ ')
        parts = command.split()
        command_name = parts[0]
        args = parts[1:]

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
        elif command_name == "touch":
            fs.mkfile()
        
        elif command_name == 'ls':
            long_format = '-l' in parts or '-la' in parts or '-al' in parts
            show_hidden = '-a' in parts or '-la' in parts or '-al' in parts
            fs.list_directory(long_format, show_hidden)
            print("ls received")
            if '-l' in args:
                fs.current_directory.list_contents()
            else:
                fs.current_directory.list_contents()

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
        
        elif command_name == 'cd':
            if parts:
                fs.change_directory(parts)
            else:
                home_directory = os.path.expanduser('~')
                fs.change_directory(home_directory)
            # fs.change_directory()

        elif command_name =='exit':
            break


        else:
            print(f'Unknown command: {command_name}')
        
        # Similar blocks for other commands...

if __name__ == "__main__":
    main()
