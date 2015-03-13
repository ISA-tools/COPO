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

brew install mysql
brew install redis
brew install mongodb

sh ./createdb.sh copo_development fshaw Apple123

# bodge needed to getg migrations working
# go into web_copo/migrations and find initial migration, then comment out the line in dependencies
# ('chunked_upload', '0001_initial'),
# then perform 'python manage.py makemigrations'
# uncomment and rerun, then migrate