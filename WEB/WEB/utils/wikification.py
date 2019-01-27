import requests, json
from nltk import sent_tokenize
import wikipediaapi


def add_link(text):
    json_request = {"text": text, "spans": []}
    response = requests.post("http://thor.nlplab.cc:5555", json=json_request)
    wiki = wikipediaapi.Wikipedia('en')
    keywords_description = {}
    for start, str_len, wiki_page in response.json():
        if wiki_page not in keywords_description:
            page = wiki.page(wiki_page)
            keywords_description[wiki_page] = sent_tokenize(page.summary)[0]

    result = ""
    start_idx = 0
    wiki_url_pre = "https://en.wikipedia.org/wiki/"
    for start, str_len, wiki_page in response.json():
        result += text[start_idx:start]
        page = (
                   """<a target="_blank" href="%s" title="%s" data-toggle="popover" data-trigger="hover" data-placement="bottom" data-content="%s">%s</a>""") % (
               wiki_url_pre + wiki_page, wiki_page, keywords_description[wiki_page], text[start: start + str_len])
        result += page

        start_idx = start + str_len
    result += text[start_idx: len(text)]
    return result


def add_wiki_link(content):
    wiki_content = []
    for tag, sentences in content:

        wiki_sentences = []
        for idx in range(len(sentences)):
            wiki_sentences.append(add_link(sentences[idx]))
        wiki_content.append([tag, ' '.join(wiki_sentences)])

    return wiki_content