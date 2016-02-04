#!/home/ubuntu/hackbop2016Feb/bin/python
from PIL import Image
import imagehash
import distance
import urllib2 as urllib
import io

"""
Demo of hashing
"""
def find_similar_images_by_url(inputUrl):
    #inputUrl = "https://s3.amazonaws.com/treblalee.images/kates4273592641_p1_1-0._SH20_QL90_UY295_.jpg"
    #inputUrl = "https://s3.amazonaws.com/treblalee.images/alice4392863185_p1_1-0._SH20_QL90_UY295_.jpg"
    return find_similar_images("/home/ubuntu/hackbop2016Feb/testImages", imagehash.dhash, inputUrl)

def find_similar_images(userpath = "/home/ubuntu/hackbop2016Feb/testImages", hashfunc = imagehash.dhash, inputUrl = "https://s3.amazonaws.com/treblalee.images/alice4392863185_p1_1-0._SH20_QL90_UY295_.jpg"):
    import os
    def is_image(filename):
    	f = filename.lower()
    	return f.endswith(".png") or f.endswith(".jpg") or \
    		f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif")

    fd = urllib.urlopen(inputUrl)
    image_file = io.BytesIO(fd.read())
    inputHash = str(hashfunc(Image.open(image_file)))
    
    image_filenames = [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
    simList = []
    for img in sorted(image_filenames):
    	hash = str(hashfunc(Image.open(img)))
        dist = distance.hamming(inputHash, hash)
        #print inputHash + " " + hash + " " + str(dist)
        if dist < 10 and dist > 0:
    	    simList.append(img.replace('/home/ubuntu/hackbop2016Feb/testImages/', 'https://s3.amazonaws.com/treblalee.images/'))

    result = {}
    result["input"] = inputUrl
    result["output"] = simList 
    print result
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
    

