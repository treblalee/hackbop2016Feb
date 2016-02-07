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

HTTP_TEMPLATE_RESPONSE = """$def with (pairs)
<html>
 <body>
  <header><h1>Pleave provide an image to see similar products on Shopbop<h1></header>
  <form name="testForm" action="http://hackbop.treblalee.com" method="post" enctype="multipart/form-data">
    <p>
      Upload an image here: <input type="file" name="uploadField" value=""/>
    </p>
    <p>
      Or provide an image url here: <input type="text" name="imageUrl" value=""/>
    </p>
    <p>
      <input type="submit" value="Submit">
    </p>
  </form>
  $if len(pairs) > 0:
    <header><h2>Similar Shopbop products below<h2></header>
    $for pair in pairs:
      <p>
        <a href=\"$pair["detailPageUrl"]\">
          <img src=\"$pair["imageUrl"]\">
        </a>
      </p>
 </body>
</html>
"""


urls = (
    '/', 'home',
    '/searchImageAlbert', 'albert_search_image',
    '/searchImageJoseph', 'joseph_search_image'
)

ALBERT_SEARCH_WEBADDRESS = 'http://localhost:8000/similarbypath?image='
SEARCH_BY_URL_ADDRESS = 'http://localhost:8000/similar?image='
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

def albert_call_img_search_algorithm(uploaded_file = "", imageUrl = ""):
        if len(imageUrl) > 0:
		img_search_url = SEARCH_BY_URL_ADDRESS + imageUrl
	else:
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

	img_search_result = json.loads(img_search_result)
	return img_search_result

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

		result = albert_call_img_search_algorithm(uploaded_file)

		return json.dumps(result["output"], sort_keys=True, indent=4, separators=(',', ': '))

class joseph_search_image:
	def GET(self):
		return HTTP_GET_JOSEPH

	def POST(self):
		web_input = web.input(uploadField={})    
		print web_input.uploadField.filename
		return joseph_dummy_result()
    	

class home:
	def GET(self):
                template = web.template.Template(HTTP_TEMPLATE_RESPONSE)
		return template([])

	def POST(self):
		web_input_upload_field = web.input(uploadField={})    
		print "Received uploadField: " + web_input_upload_field.uploadField.filename
		web_input_url_field = web.input(imageUrl={})    
		print "Received imageUrl: " + web_input_url_field.imageUrl

		uploaded_file = save_image_locally(web_input_upload_field.uploadField)
		print "uploaded_file: " + uploaded_file

		result = albert_call_img_search_algorithm(uploaded_file, web_input_url_field.imageUrl)

		template = web.template.Template(HTTP_TEMPLATE_RESPONSE)

                if "output" in result:
			return template(result["output"])
                else:
			return template([])

if __name__ == "__main__":
    app.run()
