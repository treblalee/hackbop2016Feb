#! /bin/bash

aws s3 sync --storage-class REDUCED_REDUNDANCY localS3Images s3://treblalee.images
