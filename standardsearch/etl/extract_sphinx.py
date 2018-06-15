from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, SoupStrainer

def extract_section(section):
    all_text = []
    all_parts = section.contents

    section_id = section['id']

    for part in all_parts:

        if isinstance(part, str):
            text = str(part)
        else:
            text = part.get_text()
            if 'section' in part.get('class', []):
                continue

        lines = (line.strip().rstrip('¶') for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        all_text.append(text)

    return "\n".join(all_text), section_id


def extract_page(url, base_url, new_url):
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'html5lib')

    for script in soup(["script", "style"]):
        script.extract()

    page_results = []

    sections = soup(class_="section")
 
    export_url = url
    if new_url:
        export_url = new_url + url[len(base_url):]

    for section in sections:
        text, section_id = extract_section(section)
        
        title = soup.title.string.split('—')[0].strip()

        section_title = section.find(['h1', 'h2', 'h3', 'h4', 'h5']).text.rstrip('¶')

        if title != section_title:
            title = title + ' - ' + section_title

        body = {
            'url': export_url + '#' + section_id,
            'base_url': new_url or base_url,
            'text': text,
            'title': title,
        }

        page_results.append(body)

    next_button = soup(accesskey="n")
    next_url = None
    if next_button:
        next_url = next_button[0].get('href')
    
    return page_results, next_url


class ExtractSphinx:
    def process(self, source):
        results = []
        last_url = source.url
        page_results, next_url = extract_page(source.url, source.url, source.new_url)
        results.extend(page_results)

        while next_url:
            full_next_url = urljoin(last_url, next_url)
            page_results, next_url = extract_page(urljoin(last_url, next_url), source.url, source.new_url)
            results.extend(page_results)
            last_url = full_next_url
        return results


