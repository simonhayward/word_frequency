import os

import tornado.web
import tornado.wsgi

import handlers

settings = {
    "blog_title": u"Word Frequency",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
}

tornado_app = tornado.web.Application([
    (r"/", handlers.MainHandler),
], **settings)

app = tornado.wsgi.WSGIAdapter(tornado_app)