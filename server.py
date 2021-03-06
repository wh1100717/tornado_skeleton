#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import settings
import handler

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

application = tornado.web.Application(handler.handlers, **settings.server_config)

if __name__ == "__main__":
    application.listen(settings.server_port)
    tornado.ioloop.IOLoop.instance().start()
