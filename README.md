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

### Indexing a website before it is live

If you want search to work the instant a website goes live, you have a problem. The website needs to live **before** you can index it!

The feature `newurl` or `index_version` can be used to fix that; this will let you index one website, but rewrite the URLs in the index so it looks like it is another website.

You can thus put up a preview version of a website, index that but rewrite the URL's to be as they will be at launch, 
and then launch the real website - and search will work right from the start.


### Via Command line tool

Available at `ocds-doc-search-cli.py`.

You can pass:

* `-l`, `--langs`. Two letter languages codes separated by a comma. These langs will be added to the end of the constructed URL. 
* `-u`, `--url`. The base URL to scrape. Note this MUST be the full URL.
* `-n`, `--newurl`. Optional. The URL to rewrite to. Note this MUST be the full URL.

(There is also a `version` flag that can be used instead of `url`, but this gets confusing so we are going to ignore it in these docs.)

The URL's passed should be passed without a language string. All the languages you pass will then be added to the end and indexed separately. 

#### Example 1

Pass:

* `url`: `https://standard.open-contracting.org/latest/`
* `langs`: `en,es`

The website will then index `https://standard.open-contracting.org/latest/en/` and `https://standard.open-contracting.org/latest/en/`.

#### Example 2

If you want to index a beta build as the latest, pass:

* `url`: `https://standard.open-contracting.org/beta/`
* `newurl`: `https://standard.open-contracting.org/latest/`
* `langs`: `en,es`

#### Example 3

If you want to index a profile, pass the profile as part of the URL:

Pass:

* `url`: `https://standard.open-contracting.org/profiles/ppp/latest`
* `langs`: `en,es`


### Via API 

Call `/v1/index_ocds` to index a website.

Note you must provide a `secret` to avoid abuse. This is set in Django Settings.

You can pass:

* `secret`: The secret passphrase.
* `version`: The bit of the URL to version, or the bit of the URL to rewrite to. Do NOT pass a full URL.
* `index_version`: Optional. The bit of the URL to actually index. Do NOT pass a full URL.
* `langs`: Two letter languages codes separated by a comma. These langs will be added to the end of the constructed URL. 


#### Example 1

Pass:

* `secret`: `Ssssshhhhhhh!`
* `version`: `latest`
* `langs`: `en,es`

The website will then index `https://standard.open-contracting.org/latest/en/` and `https://standard.open-contracting.org/latest/en/`.

#### Example 2

If you want to index a `beta` build as the `latest`, pass:

* `secret`: `Ssssshhhhhhh!`
* `version`: `latest`
* `index_version`: `beta`
* `langs`: `en,es`

#### Example 3

If you want to index a profile, pass the profile as part of the URL bit:

Pass:

* `secret`: `Ssssshhhhhhh!`
* `version`: `profiles/ppp/latest`
* `langs`: `en,es`

## OCDS: Searching the index

Call `/v1/search`. See the `standardsearch/webapp/views.py` function for options.

Pass:

* `q`: The query to search for
* `base_url`: The full URL to search, including languages.

### Example

* `q`: `release package`
* `base_url`: `https://standard.open-contracting.org/latest/en/`

## HTTP or HTTPS?

The software assumes the content on the HTTP and HTTPS versions of a website are the same.

If a request was made to index a HTTP site, but a user searches against a HTTPS (or vice versa), that should not matter and it should just work.

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

