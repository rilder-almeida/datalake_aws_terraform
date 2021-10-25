#!/usr/bin/env bash

cd ecr_image && bash push_image_to_ecr.sh && aws lambda invoke --function-name UnzipCensoJob