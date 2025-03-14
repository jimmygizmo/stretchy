#! /usr/bin/env bash

# THIS SCRIPT MUST BE RUN FROM THE PROJECT ROOT DIRECTORY.

echo
echo "################################"
date
echo "################################"
echo

printf "\n############################################################\n"
printf "\nCOPYING SECRETS FOR STABLED\n"
echo


# Secret (like an API key) for "stabled"
cp -pv nogit/models/* stabled/builder/models/


##
#

