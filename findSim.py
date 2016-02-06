from PIL import Image
import imagehash
import distance
import urllib2 as urllib
import io

"""
Demo of hashing
"""
cache = {}

def find_similar_images_by_url(inputUrl):
    return find_similar_images("testImages", imagehash.dhash, inputUrl)

def find_similar_images_by_file_path(path):
    return find_similar_images("testImages", imagehash.dhash, "", "", path)

def find_similar_images(userpath = "testImages", hashfunc = imagehash.dhash, inputUrl = "https://s3.amazonaws.com/treblalee.images/107.jpg", base64Image = "", inputFilePath = ""):
    import os
    global cache

    def is_image(filename):
    	f = filename.lower()
    	return f.endswith(".png") or f.endswith(".jpg") or \
    		f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif")

    # get image url to detail page mapping
    imageToDetailPageMapping = {}
    mappingFile = open("imageUrlToDetailPageMapping.txt")
    for line in mappingFile:
        fields = line.strip("\n").split(",")
        imageUrl = str(urllib.unquote(fields[0]).decode('utf8'))
        detailPageUrl = str(urllib.unquote(fields[1]).decode('utf8'))
        imageToDetailPageMapping[imageUrl] = detailPageUrl

    # compute hash of input image
    if len(inputFilePath) > 0:
        image_file = inputFilePath
        inputAsString = inputFilePath
    else:
        fd = urllib.urlopen(inputUrl)
        image_file = io.BytesIO(fd.read())
        inputAsString = inputUrl
    inputHash = str(hashfunc(Image.open(image_file)))
    
    # compute hashes of all images in DB (currently just a directory)
    image_filenames = [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
    simList = []
    for img in sorted(image_filenames):
        if img in cache:
            hash = cache[img]
        else:
    	    hash = str(hashfunc(Image.open(img)))
            cache[img] = hash
        dist = distance.hamming(inputHash, hash)
        print inputHash + " " + hash + " " + str(dist)
        if dist < 6 and dist > 0:
            imageUrl = img.replace('testImages/', 'https://s3.amazonaws.com/treblalee.images/')
            detailPageUrl = imageToDetailPageMapping[imageUrl]
            pair = {}
            pair["imageUrl"] = imageUrl
            pair["detailPageUrl"] = detailPageUrl
    	    simList.append(pair)

    result = {}
    result["input"] = inputAsString
    result["output"] = simList 
    #print result
    return result


if __name__ == '__main__':
    import sys, os
    def usage():
    	sys.stderr.write("""SYNOPSIS: %s [ahash|phash|dhash] [<directory>]

Identifies similar images in the directory.

Method: 
  ahash: Average hash
  phash: Perceptual hash
  dhash: Difference hash

(C) Johannes Buchner, 2013
""" % sys.argv[0])
    	sys.exit(1)
    
    hashmethod = sys.argv[1] if len(sys.argv) > 1 else usage()
    if hashmethod == 'ahash':
    	hashfunc = imagehash.average_hash
    elif hashmethod == 'phash':
    	hashfunc = imagehash.phash
    elif hashmethod == 'dhash':
    	hashfunc = imagehash.dhash
    else:
    	usage()
    userpath = sys.argv[2] if len(sys.argv) > 2 else "."
    find_similar_images(userpath=userpath, hashfunc=hashfunc)
    

