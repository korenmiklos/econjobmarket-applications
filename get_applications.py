import requests
from lxml import etree
import re
import os
from base64 import b64decode
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

def blob_to_file(blob_base64, file_name):
	with open(file_name, 'bw') as f:
		f.write(b64decode(blob_base64))

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

	def save_blob(self, blob_id, path):
		response = self.get_xml('Blob/%s' % blob_id)
		if response is not None:
			blob_to_file(response.text, path)

	def save_response(self, path, response):
		FORMATS = dict(cv='pdf', jmpaper='pdf', other='pdf', photo='jpeg')

		if 'type' in response and response['type'] in FORMATS:
			# simply skip over other response types
			file_name = '%s/%s.%s' % (path, response['type'], FORMATS[response['type']])
			blob_id = response['varstring']
			self.save_blob(blob_id, file_name)

	def save_reference(self, path, reference):
		file_name = '%s/reference_%s.pdf' % (path, slugify('%s %s' 
			% (reference['fname'], reference['lname'])))
		blob_id = reference['letter']
		self.save_blob(blob_id, file_name)

if __name__ == '__main__':
	connection = Connection(DATABASE, USERNAME, PASSWORD)
	applications = connection.get_list_applications()

	for aid in applications:
		application = connection.get_application(aid)
		path = slugify('%s %s %s' 
			% (application['lname'], application['mname'], application['fname'])
			) 
		os.makedirs('./%s' % path)
		print(path)
		for posid, position in application['application'].items():
			for response in position['responses']:
				connection.save_response(path, response)
			for reference in position['references']:
				connection.save_reference(path, reference)

