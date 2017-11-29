import requests
from lxml import etree
import re
from settings import *

SLUG_REGEX = re.compile('^[A-Za-z_]\w{0,64}$')

try:
    import unidecode
    def slugify(verbose_name):
        slug = re.sub(r'\W+','_',unidecode.unidecode(verbose_name).lower())
        if not SLUG_REGEX.match(slug):
            slug = '_'+slug
        return slug 
except:
    def slugify(verbose_name):
        slug = re.sub(r'\W+','_',verbose_name.lower())
        if not SLUG_REGEX.match(slug):
            slug = '_'+slug
        return slug 

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

	def get_application(self, aid):
		return self.get_json('Applicant/%s' % aid)

	def get_list_applications(self):
		application_list = self.get_json('Data')
		return [item['aid'] for item in application_list]

if __name__ == '__main__':
	connection = Connection(DATABASE, USERNAME, PASSWORD)
	applications = connection.get_list_applications()
	for aid in applications:
		application = connection.get_application(aid)
		print(slugify('%s %s %s' 
			% (application['lname'], application['mname'], application['fname'])
			))