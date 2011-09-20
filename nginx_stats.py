#!/usr/local/bin/python
import sys, re, urllib2

nginx_url = 'http://examle.com/nginx-status'
nginx_re = '^\s+\d+\s+\d+\s+\d+\s+$'

fields = ('accepts', 'handled', 'requests')

def get_data():
    site = urllib2.urlopen(nginx_url)
    data = site.read()
    site.close()
    for item in data.split('\n'):
        if re.search(nginx_re, item):
            for i in range(len(fields)):
                print 'nginx_%s.value %s' % (fields[i], item.split()[i])

def configure():
    print 'graph_title Nginx stats'
    print 'graph_args --base 1000 -l 0'
    print 'graph_scale no'
    print 'graph_vlabel Nginx requests'
    print 'graph_info This graph show nginx requests'
    print 'graph_order',
    for element in fields:
        print ' %s' % element,
    print
    for element in fields:
        print 'nginx_%s.label %s' % (element, element)
        print 'nginx_%s.type COUNTER' % element
        print 'nginx_%s.min 0' % element
        print 'nginx_%s.draw LINE1' % element
        print 'nginx_%s.info Nginx %s' % (element, element)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        configure()
        sys.exit(0)

    get_data()
