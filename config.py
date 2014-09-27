import os

#Database information
#DATABASE='blogger.db'

SQLALCHEMY_DATABASE_URI='mysql://root:password@127.0.0.1/blogger'


#Debug information
DEBUG=True

#generate the application randomkey on startup
SECRET_KEY= os.urandom(24)

#The current application username and password
USERNAME='admin'
PASSWORD='admin'

#Forms secret key
WTF_CRSF_SECRET_KEY = os.urandom(24)

#pagination
POSTS_PER_PAGE = 2
