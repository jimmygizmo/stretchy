#! /usr/bin/env bash

# THIS SCRIPT MUST BE RUN FROM THE PROJECT ROOT DIRECTORY.


echo
echo "################################"
date
echo "################################"
echo

docker build -t docker.io/jimmygizmo/gizmorepo:stretchy-stretchyagent stretchyagent
echo


##
#

