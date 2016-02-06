#! /bin/bash

aws s3 sync --storage-class REDUCED_REDUNDANCY testImages s3://treblalee.images
