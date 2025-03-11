#! /usr/bin/env bash

# THIS SCRIPT MUST BE RUN FROM THE PROJECT ROOT DIRECTORY.

echo
echo "################################"
date
echo "################################"
echo

printf "\n############################################################\n"
printf "\nCOPYING SECRETS FOR STETCHYAGENT\n"


# Secret (like an API key) for "rpagent"
cp -pv nogit/secret-stretchyagent.txt stretchyagent/


##
#

