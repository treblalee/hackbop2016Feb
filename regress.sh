#! /bin/bash

ENDPOINT='http://ec2-54-152-49-181.compute-1.amazonaws.com:8000/similar?image=https://s3.amazonaws.com/treblalee.images/colym3002512010_p1_1-0._SH20_QL90_UY295_PIshopbop-db-sticker-2,BottomRight,1,1_UY295_.jpg'
echo "Result of http get request for $ENDPOINT"
curl -XGET $ENDPOINT
echo
