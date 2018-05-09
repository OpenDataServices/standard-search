import os
import json

import standardsearch.etl.extractbs4 as extractbs4

"""
Main Process class, that calls specific process classes to do actual work.

The reason for this is that it's not clear at this stage which method will field the best results (bs4, lxml, etc).
It may even turn out that different methods will be better for different pages.
In this way, we can work on several alternative methods at once.
"""


class Extract:
    sources = []
    defaultprocess = None

    def __init__(self):
        self.defaultprocess = extractbs4.ExtractBS4()

    def add_source(self, source):
        self.sources.append(source)

    def go(self):
        output = []
        for source in self.sources:
            # For now, everything is processed with the default process.
            # In the future, maybe different sources could specify the method to use?
            output.append(self.defaultprocess.process(source))

        this_dir = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(this_dir, '../../extracted_data.json'), 'w+') as f:
            json.dump(output, f, indent=2)



