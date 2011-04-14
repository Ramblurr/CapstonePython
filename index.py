#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import os, glob, time, json, urlparse, re
from datetime import datetime
from web import form
import cassandrabase
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis

urls = ( '/', 'index',
         '/cassandra', 'cassandra',
         '/cassandra/(.*)', 'cassandra',
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

def get_seed():
    ip_store = "current_seed.txt"
    with open(ip_store, "r") as f:
        return f.read()

def set_seed(ip):
    ip_store = "current_seed.txt"
    with open(ip_store, "w") as f:
        f.write(ip)
class seed:
    def GET(self):
        return get_seed()

    def POST(self):
        ip_address = web.input()['ip']
        set_seed(ip_address)
class index:
    def GET(self):
        return "Hello"
class cassandra:
    def GET(self, args = None):
        # /cassandra or /cassandra/
        if args is None or len(args) == 0:
            # regular form page
            return render.index("hi")
        print "GET " +args
        #/cassandra/symbol/exists
        if re.match("symbol/exists", args):
            self.GET_exists(args)
        #/cassandra/symbol/search
        elif re.match("symbol/search", args):
            self.GET_search(args)
        #/cassandra/symbol/daterange
        elif re.match("symbol/daterange", args):
            self.GET_daterange(args);

    def GET_exists(self, args):
        qs = urlparse.parse_qs(web.ctx.query[1:])
        print "sym exists: %s" %( web.ctx.query[1:])
        if 'symbol' not in qs:
            return "Error"
        term = qs['symbol'][0]
        cass = cassandrabase.CassandraBase()
        cass.connect(get_seed())
        results = cass.sym_exists(term)
        return json.dumps(results)

    def GET_search(self, args):
        qs = urlparse.parse_qs(web.ctx.query[1:])
        if 'term' not in qs:
            return "Error"
        term = qs['term'][0]
        cass = cassandrabase.CassandraBase()
        cass.connect(get_seed())
        results = cass.get_symbols_by_partial(term)
        return json.dumps(results)

    def GET_daterange(self, args):
        qs = urlparse.parse_qs(web.ctx.query[1:])
        if 'term' not in qs:
            return "Error"
        term = qs['term'][0]
        cass = cassandrabase.CassandraBase()
        cass.connect(get_seed())
        results = cass.get_date_range_by_sym(term)
        return json.dumps(results)


    def getMonth(self, x):
        return {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }.get(x, "ERROR")


    def POST(self):
        form = request()
        if not form.validates():
            return "Failure. Did you select an option for all the fields?"
        sym = form['symbol'].value
        start_string = form['startdate'].value
        end_string = form['enddate'].value


        date_format = "%Y-%m-%d"
        start = datetime.strptime(start_string, date_format).strftime("%Y-%m-%d")
        end = datetime.strptime(end_string, date_format).strftime("%Y-%m-%d")

        cass = cassandrabase.CassandraBase()
        cass.connect(get_seed())

        start_time = time.time()
        records = cass.get_by_sym_range2(sym, start, end)
        if len(records) == 0:
            message = "Zero records returned. Perhaps the date range is incorrect?"
            return render.error(message)
        records_unsorted = []
        print "number records: %s" %(len(records))
        for r in records:
	    temp = r[1]
            temp['date'] = datetime.strptime(str(temp['date']), "%Y-%m-%d")
            records_unsorted.append(temp)

        records_processed = sorted(records_unsorted, key = lambda k: k['date'])
        elapsed_time = (time.time() - start_time)

        y_max = 0.0
        y_min = 0.0
        data = []
        for q in records_processed:
            temp = float(q['price_adj_close'])
                data.append(temp)
            if temp > y_max:
            y_max = temp

        y_min = y_max

        for d in records_processed:
            temp = float(d['price_adj_close'])
            if temp <  y_min:
            y_min = temp

        difference = float(y_max - y_min)
        difference = float(difference/2)

        y_min_foo = y_min-difference
        y_max_foo = y_max+difference

        if y_min_foo < 0:
            y_min_foo = 0

        chart = SimpleLineChart(1000, 300, y_range=[y_min_foo, y_max_foo])

        chart.add_data(data)
        chart.set_colours(['0000FF'])
#	chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.1, 'FFFFFF', 0.2)
#	chart.set_grid(0, 25, 5, 5)

#	y_max_output = y_max + difference
#	left_axis = range(y_min_foo, y_max_foo, 1.00)
#	left_axis[0] = y_min

        left_axis = []
        label = y_min_foo
        delta_y = 1.00
        derp = float(y_max_foo - y_min_foo)
#	if derp > 15.0:
        delta_y = derp/(10.00)

        while y_min_foo < y_max_foo:
            left_axis.append(y_min_foo)
            y_min_foo = y_min_foo + delta_y

        if len(left_axis) < 10:
            left_axis.append(y_min_foo)

        lines = len(left_axis)-1
        chart.set_grid(0, lines, 1, 1)

        x_labels = []

        for t in records_processed:
            label = (self.getMonth(t['date'].month ), t['date'].year)
            if not label in x_labels:
                x_labels.append( label )

        chart.set_axis_labels(Axis.LEFT, left_axis)
        chart.set_axis_labels(Axis.BOTTOM, x_labels)
        list_len = float(len(x_labels))
        top = float(1)
        stripe_len = float(top /list_len)
        chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', stripe_len, 'FFFFFF', stripe_len)
        imgURL = chart.get_url()

        return render.results(sym, records_processed, elapsed_time, imgURL)

class static:
    # static whitelist
    def __init__(self):
        self.whitelist = [ 'resources/main.css', 'resources/images/*', 'resources/jquery.validate.min.js' ]

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
