#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import os, glob
import datetime
from web import form

urls = ( '/', 'index',
         '/res/(.*)', 'static')
render = web.template.render('resources/')
app = web.application(urls, globals())

request = form.Form (
	form.symbol('Symbol', form.notnull),
	form.startdate('Start Date', form.notnull),
	form.enddate('End Date', form.notnull),
	form.submit('Request', type="submit"),
)

class index:
    def GET(self):
        return render.index("hi")

    def POST(self):
	form = form.request()
	if not form.validates():
		return "Failure. Did you select an option for all the fields?"
	sym = form['Symbol'].value
	start_string = form['Start Date'].value
	end_string = form['End Date'].value
	date_format = "%Y/%m/%d"
	start = datetime.strptime(start_string, date_format)
	end = datetime.strptime(end_string, date_format)

	cass = cassandrabase.CassandraBase()
	result = case.get_by_sym_range(sym, start, end)
	return result


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
