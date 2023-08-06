from filesystem import FileSystem

def main():
    fs = FileSystem()
    while True:
        command = input('$ ')
        fs.parse_command(command)

if __name__ == "__main__":
    main()