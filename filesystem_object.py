# filesystem_object.py
import os
import stat
import pwd
import grp

class FileSystemObject:
    def __init__(self, path, owner, group, permission):
        self.path = path
        self.owner = owner
        self.group = group
        self.permission = permission

    def change_permission(self, permission):
        os.chmod(self.path, int(str(permission), 8))
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