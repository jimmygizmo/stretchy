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
echo "---->  PREPARING TO BUILD STABLED"
./auto/build-034-prep-docker-build--stabled.sh


echo
echo "---->  PREPARING TO BUILD STRETCHYAGENT"
./auto/build-040-prep-docker-build--stretchyagent.sh


echo
echo "---->  BUILDING + TAGGING RPAGENT"
./auto/build-050-docker-build-tag--rpagent.sh


echo
echo "---->  BUILDING + TAGGING STABLED"
./auto/build-054-docker-build-tag--stabled.sh


echo
echo "---->  BUILDING + TAGGING STRETCHYAGENT"
./auto/build-060-docker-build-tag--stretchyagent.sh


##
#

