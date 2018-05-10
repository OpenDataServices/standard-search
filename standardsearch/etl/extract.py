import os
import json


"""
Main Process class, that calls specific process classes to do actual work.

The reason for this is that it's not clear at this stage which method will field the best results (bs4, lxml, etc).
It may even turn out that different methods will be better for different pages.
In this way, we can work on several alternative methods at once.
"""


class Extract:
    sources = []
    defaultprocess = None

    def add_source(self, source):
        self.sources.append(source)

    def go(self):
        output = []
        for source in self.sources:
            output.extend(source.extract())

        this_dir = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(this_dir, '../../extracted_data.json'), 'w+') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)



