#!/bin/bash

#assumes pip and homebrew are installed

sudo pip install django
sudo pip install djangorestframework
sudo pip install markdown       
sudo pip install django-filter  
sudo pip install django-chunked-upload
sudo pip install --allow-all-external mysql-connector-python
sudo pip install mongokit
sudo pip install mysql-python
sudo pip install jsonpickle
sudo pip install elementtree --allow-external elementtree --allow-unverified elementtree
sudo pip install lxml
sudo pip install pysam
sudo pip install bson

brew install mysql
brew install redis
brew install mongodb

sudo chown -R _mysql /usr/local/var/mysql
sudo mysql.server start
sh ./createdb.sh copo_development fshaw Apple123

sudo mkdir /data
sudo mkdir /data/db
mongod

# bodge needed to getg migrations working
# go into web_copo/migrations and find initial migration, then comment out the line in dependencies
# ('chunked_upload', '0001_initial'),
# sudo manage.py syncdb
# sudo manage.py makemigrations chunked_upload
# uncommment chunked_upload
# sudo manage.py makemigrations
# then perform 'python manage.py makemigrations'
# uncomment and rerun, then migrate