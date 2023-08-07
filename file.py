# file.py
from filesystem_object import FileSystemObject
import os

class File(FileSystemObject):
    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, content):
        with open(self.path, 'w') as f:
            f.write(content)

    def delete(self):
        os.remove(self.path)