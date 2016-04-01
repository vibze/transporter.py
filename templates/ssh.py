from transporter.interfaces.ssh.ssh import SSH


class DataStoreNameGoesHere(SSH):
    host = '127.0.0.1'   # Remote server host
    user = 'root'        # Remote server user
    pwd = 'root'         # Remote server user password
    port = 22            # Connection port