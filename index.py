#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import os, glob, time
from datetime import datetime
from web import form
import cassandrabase

urls = ( '/', 'index',
         '/results', 'results',
         '/seed', 'seed',
         '/res/(.*)', 'static')
render = web.template.render('resources/')
app = web.application(urls, globals())

request = form.Form (
	form.Textbox('symbol', form.notnull),
	form.Textbox('startdate', form.notnull),
	form.Textbox('enddate', form.notnull),
	form.Button('Request', type="submit")
)

ip_address = ""

class seed:
    def GET(self):
        global ip_address
        return ip_address

    def POST(self):
        global ip_address
        ip_address = web.input()['ip']

class index:
    def GET(self):
        return render.index("hi")

    def POST(self):
        form = request()
        if not form.validates():
            return "Failure. Did you select an option for all the fields?"
        sym = form['symbol'].value
        start_string = form['startdate'].value
        end_string = form['enddate'].value


        date_format = "%m/%d/%Y"
        start = int(datetime.strptime(start_string, date_format).strftime("%Y%m%d"))
        end = int(datetime.strptime(end_string, date_format).strftime("%Y%m%d"))

        cass = cassandrabase.CassandraBase()
        global ip_address
        cass.connect(ip_address)

        start_time = time.time()
        records = cass.get_by_sym_range(sym, start, end)
        records_unsorted = []
        for r in records:
            tmp = r[1]
            tmp['date'] = datetime.strptime(str(tmp['date']), "%Y%m%d").strftime("%Y-%m-%d")
            records_unsorted.append(tmp)
            
	records_processed = sorted(records_unsorted, key = lambda k: k['date'])
        elapsed_time = (time.time() - start_time)

#	y_max = 0
#	for(q in records_processed)
#		temp = q[1]
#		if(temp['stock_price_adj_close'] > y_max)
#			y_max = temp['stock_price_adj_close']
#		
#	chart = SimpleLineChart(400, 400, y_range=[0, y_max])
#	data = []
#	for(s in records_process)
#		temp = s[1]
#		data.append('temp[stock_price_adj_closed'])
	
#	chart.add_data(data)
#	chart.set_colours(['0000FF'])
#	chart.fill_linear_stripes(Chart.CHART, 0, CCCCCC, 0.2, 'FFFFFF', 0.2)
#	chart.set_grid(0, 25, 5, 5)

#	left_axis = range(0, max_y + 1, 25)
#	left_axis[0] = ''
#	chart.set_axis_labels(Axis.LEFT, left_axis)

#	x_labels = []
#	x_counter = 0
#	for(t in records_processed)	
#		x_counter = records_processed[1]['date']:

        return render.results(sym, records_processed, elapsed_time)


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
