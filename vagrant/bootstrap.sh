#!/bin/bash

set -e

# Install some requirements
apt-get update
apt-get install -y apt-transport-https openjdk-8-jre python3-pip apache2

# Add Elasticsearch repo and install
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -

echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list

apt-get update && apt-get install elasticsearch

# Configure Elasticsearch and restart
echo "network.host: 0.0.0.0" >> /etc/elasticsearch/elasticsearch.yml

/etc/init.d/elasticsearch restart

systemctl enable elasticsearch

# Install Python Libs
pip3 install -r /vagrant/requirements.txt
pip3 install flake8

# Install standard docs
git clone https://github.com/open-contracting/standard.git
cd standard
pip3 install -r requirements.txt
sed -i 's/www.standard-search.default.opendataservices.uk0.bigv.io/localhost:5000/g' src/standard-theme/standard_theme/static/js/search.js
make

# Configure Apache
cp /vagrant/vagrant/apache.conf  /etc/apache2/sites-enabled/000-default.conf
/etc/init.d/apache2 restart

