#!/bin/bash

sudo apt-get install python3-dev libmysqlclient-dev
sudo add-apt-repository 'deb http://archive.ubuntu.com/ubuntu bionic main'
sudo apt update
sudo apt install -y python-mysqldb
