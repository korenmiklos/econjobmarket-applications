import requests
from lxml import etree
from settings import *

class Connection(object):
	def __init__(self, database, username, password):
		self.database = database
		self.username = username
		self.password = password

	def _request(self, url):
		URL = 'https://backend.econjobmarket.org/rest/%s/%s' % (self.database, url)
		response = requests.get(URL, auth=(self.username, self.password))
		if response.status_code==200:
			return response
		else:
			return None

	def get_json(self, url):
		response = self._request('JSON/%s' % url)
		if response:
			return response.json()
		else:
			return None

	def get_xml(self, url):
		response = self._request('XML/%s' % url)
		if response:
			return etree.XML(response.text)
		else:
			return None

if __name__ == '__main__':
	connection = Connection(DATABASE, USERNAME, PASSWORD)
	print(connection.get_json('Data'))	