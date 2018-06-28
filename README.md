# standard-search

## Notes

    vagrant up
    vagrant ssh
    cd /vagrant
    python3 ocds-doc-search-cli.py -u http://localhost:6060/   # this indexes to elasticsearch
    python3 manage.py runserver 0.0.0.0:5000

Try this on the host.

  *  http://localhost:6060/en
  *  http://localhost:6060/fr
  *  http://localhost:6060/es

