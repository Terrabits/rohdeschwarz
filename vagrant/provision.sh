#!/usr/bin/env bash

# Silent
export DEBIAN_FRONTEND=noninteractive

# Update package list
sudo apt-get update

# Linux security updates
# sudo apt-get install unattended-upgrade
# sudo unattended-upgrade

# Curl
# sudo apt-get install curl

# Build tools
# sudo apt-get install build-essential

# pyenv
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
echo "export PATH=\"/home/vagrant/.pyenv/bin:\$PATH\"" >> ~/.bash_profile
echo "eval \"\$(pyenv init -)\"" >> ~/.bash_profile
echo "eval \"\$(pyenv virtualenv-init -)\"" >> ~/.bash_profile
pyenv update