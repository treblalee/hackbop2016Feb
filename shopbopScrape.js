// run in chrome console on shopbop browse page

INIT_INDEX = 0

// get the products
products = []
containers = $('.border-container .photo')
for(var i in containers.toArray()) {
 c=containers[i]
 detailPage = 'www.shopbop.com' + $(c).attr('href')
 pic = $(c).find('img').attr('src')

 products.push({'detail': detailPage,'pic': pic.trim()})
}

// get the curl string
curl_str=''

for (i=0; i<products.length; ++i) {

  splitted_pic = products[i].pic.split('/')
  img_name = INIT_INDEX+i 

  curl_str+='curl ' + products[i].pic + ' > ' + img_name + '.jpg' + '\n'
}

// get the metadata str
metadata_str=''
for (i=0; i<products.length; ++i) {
 detailPage = products[i].detail
 pic = products[i].pic
 img_name = INIT_INDEX+i 

  metadata_str+='https://s3.amazonaws.com/treblalee.images/' + img_name +'.jpg,' + detailPage + '\n'
}

// use the following two js queries to copy the respective variables to clipboard
//copy(curl_str)
//copy(metadata_str)
