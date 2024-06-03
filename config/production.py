from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'masterpiece.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xec\x14\x00\xe9\xc6FH\xf7\xf6\xe3\x06\xb0l.\xb9z'