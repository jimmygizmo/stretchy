#! /usr/bin/env bash


# STRETCHYAGENT SETUP  TODO: CUSTOMIZE!
# TODO: This was originally from "rpagent". Customize it for "stretchyagent".


# Stop script on error
set -e

# Update System
apt-get update && apt-get upgrade -y

# Install System Dependencies
# - openssh-server: for ssh access and web terminal
apt-get install -y --no-install-recommends software-properties-common gpg-agent curl git openssh-server

# Install Python 3.10
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update && apt-get install -y --no-install-recommends python3.10 python3.10-dev python3.10-distutils
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install pip for Python 3.10
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Set Python 3.10 as default
apt-get install -y python-is-python3 python-dev-is-python3

# Clean up
apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*


##
#


# TODO: This was originally from "rpagent". Customize it for "stretchyagent".

