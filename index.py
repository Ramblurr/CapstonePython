#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import os, glob
from web import form

urls = ( '/', 'index',
         '/results', 'results',
         '/res/(.*)', 'static')
render = web.template.render('resources/')
app = web.application(urls, globals())

request = form.Form (
	form.Textbox('Symbol', form.notnull),
	form.Textbox('Start Date', form.notnull),
	form.Textbox('End Date', form.notnull),
	form.Button('Request', type="submit"),
)

class results:
    def GET(self):
        records = [
            {"date": "2011/01/01", "open": "$500.00", "close": "$501.01"},
            {"date": "2011/01/01", "open": "$500.00", "close": "$501.01"},
            {"date": "2011/01/01", "open": "$500.00", "close": "$501.01"},
            {"date": "2011/01/01", "open": "$500.00", "close": "$501.01"}
            ]
        return render.results(records)

class index:
    def GET(self):
        return render.index("hi")

    def POST(self):
	form = form.request()
	if not form.validates():
		return "Failure. Did you select an option for all the fields?"
	sym = form['Symbol'].value
	start = form['Start Date'].value
	end = form['End Date'].value
	cass = cassandrabase.CassandraBase()
	result = case.request(sym, start, end)
	output = ''	
	for record in result:
		output += record
		output += "/n"
	return output


class static:
    # static whitelist
    def __init__(self):
        self.whitelist = [ 'resources/main.css', 'resources/images/*' ]

    def in_whitelist(self, path):
        print "'%s'" % (path)
        for items in self.whitelist:
            print "'%s'" % (items)
            for item in glob.glob(items):
                print item,path
                if item == path:
                    return True
        return False

    def GET(self, path):

        if not path: # index
            path = "index.html"
        base = "resources"
        full_path = os.path.join( base, path )
        print "path " + full_path
        if not self.in_whitelist(full_path):
            return web.notfound("Sorry, the page you were looking for was not found.")
        # - static handler
        #Copyright (c) 2006-2009, Wade Alcorn
        #All Rights Reserved
        #wade@bindshell.net - http://www.bindshell.net
        #
        #   Path traversal protection
        #
        full_path = os.path.join(os.getcwd(), full_path)
        if not full_path.startswith( os.getcwd() ):
            return web.notfound("Sorry, the page you were looking for was not found.")
        if os.path.exists( full_path ) and os.path.isfile( full_path ):
            if os.access( full_path, os.R_OK ):
                fh = file( full_path, 'r')
                return fh.read()
            else:
                #
                #   The user has no privileges to read this file
                #
                return web.notfound("Sorry, the page you were looking for was not found.")

        return web.notfound("Sorry, the page you were looking for was not found.")


if __name__ == "__main__":
    app.run()
