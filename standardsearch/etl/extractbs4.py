import requests
from bs4 import BeautifulSoup


class ExtractBS4:

    def process(self, source):
        r = requests.get(source.url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
                    # kill all script and style elements

            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            text = soup.get_text()

            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)


            body = {
                'url': source.url,
                'text': text,
                'title': soup.title.string,
            }
            return body

