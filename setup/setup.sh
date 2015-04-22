#!/bin/bash

#assumes pip and homebrew are installed

sudo pip install django
sudo pip install djangorestframework
sudo pip install markdown       
sudo pip install django-filter
sudo pip install --allow-all-external mysql-connector-python
sudo pip install mongokit
sudo pip install jsonpickle
sudo pip install elementtree --allow-external elementtree --allow-unverified elementtree
sudo pip install lxml
sudo pip install pysam
sudo pip install pexpect
sudo pip install redis
sudo pip install django-redis-sessions

brew install mysql
brew install redis
brew install mongodb

sudo chown -R _mysql /usr/local/var/mysql
sudo mysql.server start
sh ./createdb.sh copo_development fshaw Apple123

sudo mkdir /data
sudo mkdir /data/db
mongod
