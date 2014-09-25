import os

#Database information
#DATABASE='blogger.db'
SQLALCHEMY_DATABASE_URI='mysql://admin2WzA6ZS:93Pg4DJc8nfr@$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/blog'
#Root User: admin2WzA6ZS
#   Root Password: 93Pg4DJc8nfr
#   Database Name: blog
#Connection URL: mysql://$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/

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
