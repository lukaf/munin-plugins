#!/usr/local/bin/python
import sys, os

# import wusu
from wusu import load
a = load.FreeBSD()

def get_data():
    data = a.parse_memory()
    print 'total_memory.value %s' % (int(data['vm.stats.vm.v_page_count']) * a.pagesize)
    print 'free_memory.value %s' % ((
        int(data['vm.stats.vm.v_free_count']) + \
        int(data['vm.stats.vm.v_inactive_count']) + \
        int(data['vm.stats.vm.v_cache_count'])) * a.pagesize)

def configure():
    print 'graph_title Memory usage'
    print 'graph_args --base 1024 -l 0'
    print 'graph_scale yes'
    print 'graph_category system'
    print 'graph_vlabel Memory usage'
    print 'graph_info This graph shows memory usage'
    print 'graph_order memory_total memory_free'
    print 'memory_total.label Memory total'
    print 'memory_total.type GAUGE'
    print 'memory_total.draw AREA'
    print 'memory_total.min 0'
    print 'memory_total.colour 008000'
    print 'memory_free.label Memory free'
    print 'memory_free.type GAUGE'
    print 'memory_free.draw LINE1'
    print 'memory_free.min 0'
    print 'memory_free.colour ff0000'

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        configure()
        sys.exit(0)

    get_data()
