import web, re
class DBInterface(object):
    def __init__(self, render, name):
        self.name = name
        self.render = render
        self.ip_store = "%s_seed.txt" % (name)

    def debug(self, msg):
        print "%s: %s" % (self.name, msg)

    def save_seed(self, ip):
        with open(self.ip_store, "w") as f:
            f.write(ip)

    def POST(self, args = None):
        if args is None or len(args) == 0:
            return self.POST_query(args)
        elif re.match("seed", args):
            self.POST_seed(args)

    def GET(self, args = None):
        self.debug("GET PATH: " + web.ctx.path)
        # legacy seed check for cassandra
        if self.name == "cassandra" and re.match("/seed", web.ctx.path):
            return self.GET_seed()

        if args is None or len(args) == 0:
            # regular form page
            # this is the same as calling render.name()
            # e.g., render.cassandra()
            return getattr(self.render, self.name)("hi")
        self.debug("GET args: " + args)
        #/dbase/symbol/exists
        if re.match("symbol/exists", args):
            return self.GET_exists(args)
        #/dbase/symbol/search
        elif re.match("symbol/search", args):
            return self.GET_search(args)
        #/dbase/symbol/daterange
        elif re.match("symbol/daterange", args):
            return self.GET_daterange(args);
        elif re.match("seed", args):
            return self.GET_seed()

    def GET_seed(self):
        with open(self.ip_store, "r") as f:
            return f.read()

    def GET_exists(self, args):
        pass

    def GET_search(self, args):
        pass

    def GET_daterange(self, args):
        pass

    def POST_seed(self, args):
        ip_address = web.input()['ip']
        self.save_seed(ip_address)

    def POST_query(self, args):
        pass