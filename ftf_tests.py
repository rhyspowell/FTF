import os
from ftf import app
import unittest
import tempfile

class BloggerTestCase(unittest.TestCase):

#Sort out the database
#	def setUp(self):
#		self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#		app.config['TESTING'] = True
#		self.app = app.test_client()
#		init_db()

#	def tearDown(self):
#		os.close(self.db_fd)
#		os.unlink(blogger.app.config['DATABASE'])

	def test_empty_db(self):
		rv = self.app.get('/')
		assert 'No entries here so far' in rv.data

#Check the whole login and logout process
	def login(self, username, password):
		return self.app.post('/login', data=dict(username=username,password=password), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def test_login_logout(self):
		rv = self.login('rhys.powell@gmail.com', 'weasel12')
		assert 'You have sucessfully logged in' in rv.data
		rv = self.logout()
		assert 'You have been logged out' in rv.data
		rv = self.login('admin', 'not the password')
		assert 'Incorrect username or password' in rv.data
		rv = self.login('not the username', 'admin')
		assert 'Incorrect username or password' in rv.data

#test messages
	def test_messages(self):
		self.login('admin','admin')
		rv = self.app.post('/add', data=dict(title='<Hello>',text='<strong>HTML</strong> allowed here'), follow_redirects=True)
		assert 'No entries here so far' not in rv.data
		assert '&lt;Hello&gt;' in rv.data
		assert '<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
	unittest.main()
