#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import TemplateUtil

class SpecificHandler(TemplateUtil.DefaultHandler):
    def get(self):
        self.write("This is the Specific Handler Page!")

class MainHandler(TemplateUtil.DefaultHandler):
    def get(self, filename):
        self.write(TemplateUtil.render_template(filename))

handlers = [
    (r"/specific_request", SpecificHandler),
    (r"^/(.*)$", MainHandler),
]