#!/usr/local/bin/python
import sys

# import wusu
from wusu import load
a = load.FreeBSD()

def get_data():
    data = a.parse_loadavg()
    print 'system_load.value %s' % data[1]

def configure():
    print 'graph_title System load average (5min)'
    print 'graph_args --base 1000 -l 0'
    print 'graph_scale no'
    print 'graph_category System'
    print 'graph_vlabel System load average in 5 min'
    print 'graph_order system_load'
    print 'system_load.label Load avg in 5min'
    print 'system_load.type GAUGE'
    print 'system_load.min 0'
    print 'system_load.draw LINE1'
    print 'system_load.info Load in 5min'

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        configure()
        sys.exit(0)

    get_data()
