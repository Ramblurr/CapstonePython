#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import os, glob

urls = ( '/seed', 'seed' )
app = web.application(urls, globals())

class seed:
    def GET(self):
        return "192.168.2.0.0"

if __name__ == "__main__":
    app.run()
