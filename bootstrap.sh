#!/bin/bash

set -e

# install brew / also includes xcode command line tools
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# install ansible
brew install ansible

