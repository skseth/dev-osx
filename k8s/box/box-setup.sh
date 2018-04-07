#!/usr/bin/env bash

# see https://serverfault.com/questions/500764/dpkg-reconfigure-unable-to-re-open-stdin-no-file-or-directory
export DEBIAN_FRONTEND=noninteractive

# setup repos for ansible, docker and certs
# (http://docs.ansible.com/intro_installation.html)
apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update

# setup docker-ce
apt-get -y install docker-ce
usermod -aG docker vagrant

# setup ansible
apt-get -y install ansible

# add root certificate to box
mkdir /usr/local/share/ca-certificates/extra
cp /home/vagrant/root.cert.pem /usr/local/share/ca-certificates/extra/root.cert.crt
update-ca-certificates
