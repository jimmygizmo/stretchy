#! /usr/bin/env bash

# THIS SCRIPT MUST BE RUN FROM THE PROJECT ROOT DIRECTORY.


echo "-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -"
echo "- - - - - - - - PUSH ALL"

echo "---->  ./auto/push-010-full-project--push-all.sh"


# AWS ecr get login password and docker login.
./auto/push-020-docker-aws-ecr-auth--docker-login.sh

sleep 1


./auto/push-030-rpagent--push-rpagent.sh


./auto/push-040-stretchyagent--push-stretchyagent.sh


##
#

