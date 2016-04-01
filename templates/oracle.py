from transporter.interfaces import Oracle


class DataStoreNameGoesHere(Oracle):
    path = None                                 # Oracle data path
    user = None                                 # Oracle username
    pwd = None                                  # Oracle password
    nls_lang = 'AMERICAN_AMERICA.CL8ISO8859P5'  # Language setting
