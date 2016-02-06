import sys
import web
import json
import os
import uuid
import urllib2

# html test forms
HTTP_GET_ALBERT = """
<html>
 <body>
  <h1>search-Image-Albert<h1>
  <form name="testForm" action="http://hackbop.treblalee.com/upload" method="post" enctype="multipart/form-data">
   <input type="file" name="uploadField"/>
   <input type="submit" value="Submit">
  </form>
 </body>
</html>
"""

HTTP_GET_JOSEPH = """
<html>
 <body>
  <h1>search-Image-Joseph<h1>
  <form name="testForm" action="http://ec2-54-152-49-181.compute-1.amazonaws.com:8080/searchImageJoseph" method="post" enctype="multipart/form-data">
   <input type="file" name="uploadField"/>
   <input type="submit" value="Submit">
  </form>
 </body>
</html>
"""


urls = (
    '/searchImageAlbert', 'albert_search_image',
    '/searchImageJoseph', 'joseph_search_image'
)

ALBERT_SEARCH_WEBADDRESS = 'http://localhost:8000/similarbypath?image='
IMAGE_FOLDER = '/tmp/HackbopImgs'

DEFAULT_ALBERT_RETURN = '{}'

def create_random_dir():
	path = IMAGE_FOLDER + '/' + str(uuid.uuid4())
	os.makedirs(path)
	return path

def save_image_locally(upload_file):
	file_path = create_random_dir() + '/input_' + upload_file.filename
	fout = open(file_path,'w')
	fout.write(upload_file.file.read())
	fout.close()
	return file_path

def albert_call_img_search_algorithm(uploaded_file):
	img_search_url = ALBERT_SEARCH_WEBADDRESS + uploaded_file
	print "HTTP GET: " + img_search_url

	img_search_result = DEFAULT_ALBERT_RETURN
	try:
		response = urllib2.urlopen(img_search_url)
		img_search_result = response.read()
	except urllib2.HTTPError as e:
		print 'The server couldn\'t fulfill the request: ' + img_search_url
		print 'Reason: ', e.reason
	except urllib2.URLError as e:
		print 'Failed to call to: ' + img_search_url
		print 'Reason: ', e.reason
		# TODO: raise error

	img_search_result_json = json.loads(img_search_result)

	return json.dumps(img_search_result_json['output'])

def joseph_dummy_result():
	searchUrl = 'https://www.shopbop.com/actions/viewSearchResultsAction.action?searchButton=Submit&query=Dress+Green&searchSuggestion=false'
	keyWords = ['Dress','Green']
	return json.dumps({'searchUrl':searchUrl,'keyWords':keyWords})

app = web.application(urls, globals())

class albert_search_image:
	def GET(self):
		return HTTP_GET_ALBERT

	def POST(self):
		web_input = web.input(uploadField={})    
		print "Recieved: " + web_input.uploadField.filename

		uploaded_file = save_image_locally(web_input.uploadField)
		print "uploaded_file: " + uploaded_file

		result_json = albert_call_img_search_algorithm(uploaded_file)

		return result_json

class joseph_search_image:
	def GET(self):
		return HTTP_GET_JOSEPH

	def POST(self):
		web_input = web.input(uploadField={})    
		print web_input.uploadField.filename
		return joseph_dummy_result()
    	

if __name__ == "__main__":
    app.run()