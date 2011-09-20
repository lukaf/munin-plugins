#!/usr/local/bin/python
import sys

# import wusu
from wusu import storage
a = storage.FreeBSD()

def get_data():
    data = a.parse_fsusage()
    for disk in data.keys():
        print '%s_free.value %s' % (disk, data[disk]['free'])
        print '%s_used.value %s' % (disk, data[disk]['used'])

def configure():
    print 'graph_title Disk usage in kB'
    print 'graph_args --base 1024 -l 0'
    print 'graph_scale no'
    print 'graph_category disk'
    print 'graph_vlabel Disk space usage'
    print 'graph_info This graph shows disk space usage'
    data = a.parse_fsusage()
    print 'graph_order',
    for disk in data.keys():
        print ' %s_used %s_free' % (disk, disk),
    print
    for disk in data.keys():
        print '%s_free.label %s' % (disk, disk)
        print '%s_free.type GAUGE' % disk
        print '%s_free.min 0' % disk
        print '%s_free.draw LINE1' % disk
        print '%s_free.info %s' % (disk, data[disk]['mount'])
        print '%s_used.label %s' % (disk, disk)
        print '%s_used.type GAUGE' % disk
        print '%s_used.min 0' % disk
        print '%s_used.draw AREA' % disk
        print '%s_free.info %s' % (disk, data[disk]['mount'])

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        configure()
        sys.exit(0)

    get_data()
