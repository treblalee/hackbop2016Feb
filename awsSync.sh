#! /bin/bash

IMG_ROOT='/home/ubuntu/hackbop2016Feb/testImages/'
aws s3 sync s3://treblalee.images $IMG_ROOT

