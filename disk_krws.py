import sys

# import wusu
from wusu import storage
a = storage.FreeBSD()

def get_data():
    data = a.parse_iostat()
    for disk in data.keys():
        print "%s_krs.value %s" % (disk, data[disk]['krs'].split('.')[0])
        print "%s_kws.value %s" % (disk, data[disk]['kws'].split('.')[0])

def configure():
    print 'graph_title Disk r/w per second in kB'
    print 'graph_args --base 1024 -l 0'
    print 'graph_scale no'
    print 'graph_category disk'
    print 'graph_vlabel r/w in kB'
    print 'graph_info This graph shows r/w per second in kB'
    data = a.parse_iostat()
    print 'graph_order',
    for disk in data.keys():
        print ' %s_krs %s_kws' % (disk, disk),
    print
    for disk in data.keys():
        print '%s_krs.label %s' % (disk, disk)
        print '%s_krs.type COUNTER' % disk
        print '%s_krs.min 0' % disk
        print '%s_krs.draw LINE1' % disk
        print '%s_krs.info %s r/s in kB' % (disk, disk)
        print '%s_kws.label %s' % (disk, disk)
        print '%s_kws.type COUNTER' % disk
        print '%s_kws.min 0' % disk
        print '%s_kws.draw LINE1' % disk
        print '%s_kws.info %s w/s in kB' % (disk, disk)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        configure()
        sys.exit(0)

    get_data()
