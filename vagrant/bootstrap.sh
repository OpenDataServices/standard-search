#!/bin/bash

set -e

# Install some requirements
apt-get update
apt-get install -y apt-transport-https openjdk-8-jre python3-pip apache2

pip3 install virtualenv

# Add Elasticsearch repo and install
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -

echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list

apt-get update && apt-get install elasticsearch

# Configure Elasticsearch and restart
echo "network.host: 0.0.0.0" >> /etc/elasticsearch/elasticsearch.yml

/etc/init.d/elasticsearch restart

systemctl enable elasticsearch

# Install Virtenv and Python Libs
cd /vagrant
virtualenv .ve -p python3
source .ve/bin/activate
pip3 install -r /vagrant/requirements_dev.txt
deactivate

# Install standard docs (using virtualenv)
git clone https://github.com/open-contracting/standard.git /home/vagrant/standard
cd /home/vagrant/standard
virtualenv .ve -p python3
source .ve/bin/activate
pip3 install -r requirements.txt
sed -i 's/standard-search.open-contracting.org/localhost:5000/g' .ve/src/standard-theme/standard_theme/static/js/search.js
make
deactivate

# Configure Apache
cp /vagrant/vagrant/apache.conf  /etc/apache2/sites-enabled/000-default.conf
/etc/init.d/apache2 restart

