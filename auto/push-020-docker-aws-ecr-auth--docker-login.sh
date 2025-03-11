#! /usr/bin/env bash

echo
echo "################################"
date
echo "################################"
echo

AWS_ECR_PASSWORD=$(aws ecr get-login-password --region us-west-2)

sleep 1

# TODO: This needs to be made correct for the repository to be used (Docker Hub)
# TODO: Fix this, it is incorrect, partial and came from AWS originally:
#docker login -u AWS -p $AWS_ECR_PASSWORD https://AWS--ACCOUNT--ID.hub.docker.io


##
#

