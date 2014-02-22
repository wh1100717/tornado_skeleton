#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
from tornado import httpclient
from mako import exceptions
from mako.lookup import TemplateLookup
import settings
import os

'''
This is a special Mako object, 
[TemplateLookup](http://docs.makotemplates.org/en/latest/usage.html#mako.lookup.TemplateLookup), 
that provides a simple API for secure (rooted) template lookup, retrieval, and encoding, amongst other things.
'''
template_lookup = TemplateLookup(input_encoding='utf-8',
                                 output_encoding='utf-8',
                                 encoding_errors='replace',
                                 directories=[settings.__template_dir__])

def render_template(filename, **kwargs):
    print settings.__root_dir__
    if os.path.isdir(os.path.join(settings.__template_dir__, filename)):
    	#比如说filename是`app`，而实际上`/templates/app`是个目录，则实际渲染的是`/templates/app/index.html`模板
        filename = os.path.join(filename, 'index.html')
    else:
    	#如果`app`所对应的`/templates/app`不是个目录，则渲染`/templates/app.html`
        filename = '%s.html' % filename
    if any(filename.lstrip('/').startswith(p) for p in settings.__blacklist_templates__):
    	#检测是否访问的是列入黑名单(__blacklist_templates__)的渲染目录，如果是的话，则raise error 404
        raise httpclient.HTTPError(404)
    try:
    	#如果一切正常，利用TemplateLookup进行模板渲染
        return template_lookup.get_template(filename).render(**kwargs)
    except exceptions.TopLevelLookupException:
        raise httpclient.HTTPError(404)

#extend了tornado的RequestHandler，重写了get_error_html，实现了自定义错误页面的功能
class DefaultHandler(tornado.web.RequestHandler):
    def get_error_html(self, status_code, exception, **kwargs):
        if hasattr(exception, 'code'):
            self.set_status(exception.code)
            if exception.code == 500:
                return exceptions.html_error_template().render()
            #除了code 500以外，所有的错误都会根据/template/{code}.html进行渲染
            #因此需要在/templates/下面定义对应错误信息的默认页面
            return render_template(str(exception.code))
        return exceptions.html_error_template().render()