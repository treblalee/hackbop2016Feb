#! /bin/bash

HOST='http://ec2-52-23-125-147.compute-1.amazonaws.com'
PORT='8000'
HOME_ENDPOINT="$HOST:$PORT"
SIM_ENDPOINT="$HOME_ENDPOINT/similar?image=https://s3.amazonaws.com/treblalee.images/colym3002512010_p1_1-0._SH20_QL90_UY295_PIshopbop-db-sticker-2,BottomRight,1,1_UY295_.jpg"
SIM_PATH_ENDPOINT="$HOME_ENDPOINT/similarbypath?image=testImages/colym3002512010_p1_1-0._SH20_QL90_UY295_PIshopbop-db-sticker-2,BottomRight,1,1_UY295_.jpg"
echo
echo "Result of http get request for $HOME_ENDPOINT"
curl -XGET $HOME_ENDPOINT
echo
echo
echo "Result of http get request for $SIM_ENDPOINT"
curl -XGET $SIM_ENDPOINT
echo
echo
echo "Result of http get request for $SIM_PATH_ENDPOINT"
curl -XGET $SIM_PATH_ENDPOINT
echo
echo
