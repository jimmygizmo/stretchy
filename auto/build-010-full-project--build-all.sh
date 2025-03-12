#! /usr/bin/env bash

# THIS SCRIPT MUST BE RUN FROM THE PROJECT ROOT DIRECTORY.


echo "-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -"
echo "- - - - - - - - BUILD ALL"
echo


echo "---->  ./auto/build-010-full-project--build-all.sh"


echo
echo "---->  PREPARING TO BUILD RPAGENT"
./auto/build-030-prep-docker-build--rpagent.sh


echo
echo "---->  PREPARING TO BUILD STETCHYAGENT"
./auto/build-040-prep-docker-build--stretchyagent.sh


echo
echo "---->  BUILDING + TAGGING RPAGENT"
./auto/build-050-docker-build-tag--rpagent.sh


echo
echo "---->  BUILDING + TAGGING STETCHYAGENT"
./auto/build-060-docker-build-tag--stretchyagent.sh


##
#

