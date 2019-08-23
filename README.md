# standard-search

## Welcome

Standard Search is a web app in front of Elasticsearch. 

It can be called via the API or command line and made to index a Sphinx documentation website. 
(There is a basic security mechanism on the API to prevent abuse.)

There is then another API that Javascript widgets can call to get search results, 
and in that way provide a search function on Sphinx documentation websites.

It understands the output of Sphinx, and cleverly extracts things like sections.

It currently has functions specific to OCDS, but it can easily be made to work for other standards.

## Technical requirements

* A Django app web server
* An Elasticsearch 6 server

## OCDS: Indexing a website

### Command line tool

Available at `ocds-doc-search-cli.py` - see that for the options to use.

### API 

Call `/v1/index_ocds` to index a website. See the `standardsearch/webapp/views.py` function for options.

Note you must provide a `secret` to avoid abuse. This is set in Django Settings.

### Indexing a website before it is live

If you want search to work the instant a website goes live, you have a problem. The website needs to live **before** you can index it!

The feature `newurl` or `index_version` can be used to fix that; this will let you index one website, but rewrite the URLs in the index so it looks like it is another website.

You can thus put up a preview version of a website, index that but rewrite the URL's to be as they will be at launch, 
and then launch the real website - and search will work right from the start.

## OCDS: Searching the index

Call `/v1/search`. See the `standardsearch/webapp/views.py` function for options.

## Adding other sources

It is currently set up for OCDS. 

This can be extended for other standards, but at this time we may also try to work out a generic set of interfaces.

## Vagrant for developers

A Vagrant box is provided for developers. 

This also builds a static version of the OCDS standard, so you can test it against a development website you can control.

NOTE: This is not in full working order and needs tweaks! See pull request. 

    vagrant up
    vagrant ssh
    cd /vagrant
    python3 ocds-doc-search-cli.py -u http://localhost:6060/   # this indexes to elasticsearch
    python3 manage.py runserver 0.0.0.0:5000

Try this on the host.

  *  http://localhost:6060/en
  *  http://localhost:6060/fr
  *  http://localhost:6060/es

