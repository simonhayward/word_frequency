import logging
from collections import Counter
from random import shuffle

import tornado.web
from google.appengine.api import urlfetch

from ex import RequestFailure, HTTPError
from parse import get_words

REQUEST_TIMEOUT_SECONDS = 5
MAX_WORDS = 100


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("form.html")

    def post(self):
        site_url = self.get_argument("site_url", None)
        if not site_url or not site_url.startswith("http"): 
            raise tornado.web.HTTPError(400)

        try:
            body = request(site_url)
        except RequestFailure:
            raise tornado.web.HTTPError(504)
        except HTTPError as e:
            raise tornado.web.HTTPError(e.status_code)

        top_words = get_top_words(get_words(body))
        shuffle(top_words) 
        self.render("word_cloud.html", top_words=top_words)


def request(url):
    try:
        urlfetch.set_default_fetch_deadline(REQUEST_TIMEOUT_SECONDS)
        r = urlfetch.fetch(url)
    except urlfetch.Error as e:
        logging.exception('Request failure')
        raise RequestFailure(e)
    
    if r.status_code != 200:
        raise HTTPError(e, status_code=r.status_code)

    return r.content

def get_top_words(words):
    cloud = Counter(words)
    top_words = cloud.most_common(MAX_WORDS)
    return top_words