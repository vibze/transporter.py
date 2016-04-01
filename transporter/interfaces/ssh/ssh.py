import os
from socket import socket
from stat import S_ISDIR
import errno
import paramiko


class SSHException(Exception):
    pass


class SSH(object):
    user = None
    pwd = None
    host = None
    port = 22

    def __init__(self):
        self._sftp = None

    @property
    def sftp(self):
        if not self._sftp:
            t = paramiko.Transport((self.host, self.port))
            t.connect(None, self.user, self.pwd)
            self._sftp = paramiko.SFTPClient.from_transport(t)

        return self._sftp

    def upload_directory(self, local_path, remote_path):
        """
        Upload directory to remote server

        :param local_path: local directory absolute path
        :param remote_path: remote upload directory absolute path
        :return:
        """
        self.delete_remote_dir(remote_path)

        temp_folder = ''
        for f in remote_path.split('/'):
            if f:
                temp_folder += '/%s' % f
                if not self.remote_dir_exists(temp_folder):
                    self.make_remote_dir(temp_folder)

        for f in os.listdir(local_path):
            local_f_path = os.path.join(local_path, f)
            remote_f_path = '%s/%s' % (remote_path, f)
            self.upload_file(local_f_path, remote_f_path)

    def upload_file(self, local_path, remote_path):
        """
        Upload file to remote server

        :param local_path: local absolute path
        :param remote_path: remote absolute path
        :return:
        """
        self.sftp.put(local_path, remote_path)

    def remote_dir_exists(self, path):
        """
        Check if directory on remote server already exists

        :param path: Absolute path on remote server
        :return: boolean
        """
        try:
            self.sftp.stat(path)
            return True
        except IOError, e:
            if e.errno == errno.ENOENT:
                return False

    def delete_remote_dir(self, path):
        """
        Delete directory and all of its contents on remote server

        :param path: Absolute path
        :return:
        """
        if self.remote_dir_exists(path):
            try:
                for f in self.sftp.listdir(path):
                    new_path = '/'.join((path, f))
                    if self.is_dir(new_path):
                        self.delete_remote_dir(new_path)
                    else:
                        self.sftp.remove(new_path)
                self.sftp.rmdir(path)
            except IOError:
                raise SSHException("Failed to remove dir %s" % path)

    def make_remote_dir(self, path):
        """
        Create directory on remote server

        :param path: Absolute path
        :return:
        """
        self.sftp.mkdir(path)

    def is_dir(self, path):
        try:
            return S_ISDIR(self.sftp.stat(path).st_mode)
        except IOError:
            return False