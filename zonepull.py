#!/usr/bin/env python
### Zonepuller
## Attempts to get a domain transfer from the nameservers for the given domain
## Requires dnspython http://www.dnspython.org/

import sys
import socket
import optparse
try:
    from dns import resolver, query, exception
except ImportError:
    print "This script requires dnspython"
    print "http://www.dnspython.org/"
    sys.exit(1)



class Transferrer(object):
    def __init__(self, domain):
        self.domain = domain
        ## build list of nameservers
        nss = resolver.query(domain, 'NS')
        self.nameservers = [ str(ns) for ns in nss ]


    def transfer(self):
        for ns in self.nameservers:
            print >> sys.stderr, "Querying %s" % (ns,)
            print >> sys.stderr, "-" * 50
            z = self.query(ns)
            print z
            print >> sys.stderr, "%s\n" % ("-" * 50,)


    def query(self, ns):
        nsaddr = self.resolve_a(ns)
        try:
            z = self.pull_zone(nsaddr)
        except (exception.FormError, socket.error, EOFError):
            print >> sys.stderr, "AXFR failed\n"
            return None
        else:
            return z


    def resolve_a(self, name):
        """Pulls down an A record for a name"""
        nsres = resolver.query(name, 'A')
        return str(nsres[0])


    def pull_zone(self, nameserver):
        """Sends the domain transfer request"""
        q = query.xfr(nameserver, self.domain, relativize=False, timeout=2)
        zone = ""   ## janky, but this library returns
        for m in q: ## an empty generator on timeout
            zone += str(m)
        if not zone:
            raise EOFError
        return zone


if __name__ == "__main__":
    parser = optparse.OptionParser(usage="%prog <domain>", version="%prog 0.1")
    options, args = parser.parse_args()
    if not args:
        parser.error("Must include at least one domain to transfer")

    for dom in args:
        t = Transferrer(dom)
        t.transfer()
