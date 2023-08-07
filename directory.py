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

    # def long_list_contents(self):
    #     contents = os.listdir(self.path)
    #     for name in contents:
    #         item_path = os.path.join(self.path, name)
    #         st = os.stat(item_path)
    #         details = {
    #             'name': name,
    #             'owner': pwd.getpwuid(st.st_uid).pw_name,
    #             'group': grp.getgrgid(st.st_gid).gr_name,
    #             'permission': stat.filemode(st.st_mode),
    #             'size': st.st_size,
    #             'last_modified': time.ctime(st.st_mtime)
    #         }
    #         print(details)