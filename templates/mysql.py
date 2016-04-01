from transporter.interfaces.mysql.db import MySQL


class DataStoreNameGoesHere(MySQL):
    host = '127.0.0.1'   # MySQL Network address, port can be provided with colon notation
    user = 'root'        # MySQL Username
    pwd = 'root'         # MySQL Password
    db = None            # Database to use. If None then schemaless connection will be used
    charset = 'utf8mb4'  # Default connection encoding
    print_sql = False    # Enable this if you want this interface to print queries before executing