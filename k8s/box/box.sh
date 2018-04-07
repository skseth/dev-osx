#!/usr/bin/env bash

rm local-xenial64.box
vagrant up
vagrant package --output local-xenial64.box
vagrant destroy -f localbox
vagrant box add -f local-xenial64 local-xenial64.box



