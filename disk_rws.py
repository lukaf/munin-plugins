import sys

# import wusu
from wusu import storage
a = storage.FreeBSD()

def get_data():
    data = a.parse_iostat()
    for disk in data.keys():
        print "%s_rs.value %s" % (disk, data[disk]['rs'].split('.')[0])
        print "%s_ws.value %s" % (disk, data[disk]['ws'].split('.')[0])

def configure():
    print 'graph_title Disk r/w per second'
    print 'graph_args --base 1000 -l 0'
    print 'graph_scale no'
    print 'graph_category disk'
    print 'graph_vlabel r/w'
    print 'graph_info This graph shows w/r per second'
    data = a.parse_iostat()
    print 'graph_order',
    for disk in data.keys():
        print ' %s_rs %s_ws' % (disk, disk),
    print
    for disk in data.keys():
        print '%s_rs.label %s' % (disk, disk)
        print '%s_rs.type COUNTER' % disk
        print '%s_rs.min 0' % disk
        print '%s_rs.draw LINE1' % disk
        print '%s_rs.info %s r/s' % (disk, disk)
        print '%s_ws.label %s' % (disk, disk)
        print '%s_ws.type COUNTER' % disk
        print '%s_ws.min 0' % disk
        print '%s_ws.draw LINE1' % disk
        print '%s_ws.info %s w/s' % (disk, disk)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        configure()
        sys.exit(0)

    get_data()
