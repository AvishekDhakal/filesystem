import os
import stat
import pwd
import grp
import time

class Directory:
    def __init__(self, path, owner, group, permission):
        self.path = path
        self.owner = owner
        self.group = group
        self.permission = permission

    def create_subdirectory(self, name, owner, group, permission):
        path = os.path.join(self.path, name)
        os.mkdir(path, permission)
        return Directory(path, owner, group, permission)

    def delete_subdirectory(self, name):
        path = os.path.join(self.path, name)
        os.rmdir(path)

    def list_contents(self):
        print("listing")
        return os.listdir(self.path)

    def change_permission(self, permission):
        os.chmod(self.path, permission)
        self.permission = permission

    def change_owner(self, owner, group):
        uid = pwd.getpwnam(owner).pw_uid
        gid = grp.getgrnam(group).gr_gid
        os.chown(self.path, uid, gid)
        self.owner = owner
        self.group = group

    def details(self):
        st = os.stat(self.path)
        return {
            'path': self.path,
            'owner': self.owner,
            'group': self.group,
            'permission': stat.filemode(st.st_mode),
            'size': st.st_size,
            'last_modified': st.st_mtime
        }
    def change_permission(self, permission):
        os.chmod(self.path, int(str(permission), 8))
        self.permission = permission
    
    def create_subdirectory(self, name, owner, group, permission):
        path = os.path.join(self.path, name)
        os.mkdir(path, int(str(permission), 8))
        return Directory(path, owner, group, permission)

    def long_list_contents(self):
        contents = os.listdir(self.path)
        for name in contents:
            item_path = os.path.join(self.path, name)
            st = os.stat(item_path)
            details = {
                'name': name,
                'owner': pwd.getpwuid(st.st_uid).pw_name,
                'group': grp.getgrgid(st.st_gid).gr_name,
                'permission': stat.filemode(st.st_mode),
                'size': st.st_size,
                'last_modified': time.ctime(st.st_mtime)
            }
            print(details)