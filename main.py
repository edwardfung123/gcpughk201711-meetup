#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2


class MainPage(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        from webapp2_extras import jinja2
        return jinja2.get_jinja2(app=self.app)

    def get(self):
        data = {
            'name': 'Edward',
            'd': {'foo': 'b<p style="color:red">ar</p>'},
            }
        html = self.jinja2.render_template('index.html', **data)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
