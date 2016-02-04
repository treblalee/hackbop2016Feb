from bottle import route, request, run, template
import subprocess
from findSim import find_similar_images, find_similar_images_by_url

@route('/similar')
def similar():
    inputUrl = request.query.image
    return find_similar_images_by_url(inputUrl) 

@route('/')
def home():
    return find_similar_images()

run(host='0.0.0. 0', port=8000)
