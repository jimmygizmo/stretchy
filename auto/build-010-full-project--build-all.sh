#! /usr/bin/env bash

# THIS SCRIPT MUST BE RUN FROM THE PROJECT ROOT DIRECTORY.


echo "-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -"
echo "- - - - - - - - BUILD ALL"

echo "---->  ./auto/build-010-full-project--build-all.sh"


./auto/build-030-prep-docker-build--rpagent.sh

./auto/build-040-prep-docker-build--stretchyagent.sh

# Build the nginx container.
./auto/build-050-docker-build-tag--rpagent.sh

# Build the express container.
./auto/build-060-docker-build-tag--stretchyagent.sh


##
#

