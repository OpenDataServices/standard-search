# standard-search

## Notes

    vagrant up
    vagrant ssh
    wget --method=PUT -O/tmp/create.index.txt http://localhost:9200/standardsearch
    PYTHONPATH=$PYTHONPATH:/vagrant/  python3 /vagrant/etl-demo.py
    FLASK_APP=/vagrant/standardsearch/webapp/webapp.py  PYTHONPATH=$PYTHONPATH:/vagrant/  flask run --host=0.0.0.0

Try

  *  http://localhost:5000/v1/search?q=example
  *  http://localhost:5000/v1/search?q=open

Browse demo page on

  *  http://localhost:6060/

