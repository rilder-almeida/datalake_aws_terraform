#! /usr/bin/env bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 051624633563.dkr.ecr.us-east-1.amazonaws.com

docker build -t igti-ecr-censo-image .

docker tag igti-ecr-censo-image:latest 051624633563.dkr.ecr.us-east-1.amazonaws.com/igti-ecr-censo-image:latest

docker push 051624633563.dkr.ecr.us-east-1.amazonaws.com/igti-ecr-censo-image:latest