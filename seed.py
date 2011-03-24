#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import os, glob

urls = ( '/seed', 'seed' )
app = web.application(urls, globals())

ip_address = ""

class seed:
    def GET(self):
        global ip_address
        return ip_address

    def POST(self):
        global ip_address
        ip_address = web.input()['ip']
        

if __name__ == "__main__":
    app.run()
