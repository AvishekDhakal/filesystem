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
        """
        The function changes the permission of a file or directory to the specified permission.

        """
        os.chmod(self.path, int(str(permission), 8))
        self.permission = permission

    def change_owner(self, owner, group):
        """
        The function changes the owner and group of a file or directory in Python.
        
        """
        uid = pwd.getpwnam(owner).pw_uid
        gid = grp.getgrnam(group).gr_gid
        os.chown(self.path, uid, gid)
        self.owner = owner
        self.group = group

    def details(self):
        """
        The function "details" returns various details about a file, including its path, owner, group,
        permission, size, and last modified timestamp.
        :return: a dictionary containing the following details:
        - 'path': the path of the file or directory
        - 'owner': the owner of the file or directory
        - 'group': the group of the file or directory
        - 'permission': the permission of the file or directory in the form of a string (e.g.
        'drwxr-xr-x')
        - 'size':
        """

        st = os.stat(self.path)
        return {
            'path': self.path,
            'owner': self.owner,
            'group': self.group,
            'permission': stat.filemode(st.st_mode),
            'size': st.st_size,
            'last_modified': st.st_mtime
        }