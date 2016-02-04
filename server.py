from bottle import route, request, run, template
import subprocess
from findSim import find_similar_images, find_similar_images_by_url, find_similar_images_by_file_path

@route('/similar')
def similar():
    inputUrl = request.query.image
    return find_similar_images_by_url(inputUrl) 

@route('/similarbypath')
def similar():
    inputPath = request.query.image
    return find_similar_images_by_file_path(inputPath) 

@route('/')
def home():
    return find_similar_images()

run(host='0.0.0. 0', port=8000)
