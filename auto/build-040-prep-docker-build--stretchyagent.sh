#! /usr/bin/env bash

# THIS SCRIPT MUST BE RUN FROM THE PROJECT ROOT DIRECTORY.

echo
echo "################################"
date
echo "################################"
echo

printf "\n############################################################\n"
printf "\nCOPYING SECRETS FOR STRETCHYAGENT\n"
echo


# Secret (like an API key) for "stretchyagent"
cp -pv nogit/secret-stretchyagent.txt stretchyagent/


##
#

