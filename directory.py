# directory.py
from filesystem_object import FileSystemObject
import os,pwd,stat,grp,time

class Directory(FileSystemObject):
    def create_directory(self, name, owner, group, permission):
        path = os.path.join(self.path, name)
        os.mkdir(path, int(str(permission), 8))
        return Directory(path, owner, group, permission)

    def delete_directory(self, name):
        path = os.path.join(self.path, name)
        os.rmdir(path)

    def list_contents(self):
        return os.listdir(self.path)
