
import standardsearch.elasticsearchfactory
import standardsearch.etl.processbs4

"""
Main Process class, that calls specific process classes to do actual work.

The reason for this is that it's not clear at this stage which method will field the best results (bs4, lxml, etc).
It may even turn out that different methods will be better for different pages.
In this way, we can work on several alternative methods at once.
"""


class Process:
    elasticsearchfactory = None
    sources = []
    defaultprocess = None

    def __init__(self):
        self.elasticsearchfactory = standardsearch.elasticsearchfactory.ElasticSearchFactory()
        self.defaultprocess = standardsearch.etl.processbs4.ProcessBS4(self.elasticsearchfactory)

    def add_source(self, source):
        self.sources.append(source)

    def go(self):
        for source in self.sources:
            # For now, everything is processed with the default process.
            # In the future, maybe different sources could specify the method to use?
            self.defaultprocess.process(source)
