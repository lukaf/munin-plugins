import sys

# import wusu
from wusu import storage
a = storage.FreeBSD()

def get_data(): 
    data = a.parse_iostat()
    for disk in data.keys():
        print "%s_wait.value %s" % (disk, data[disk]['wait'])

def configure():
    print 'graph_title Disk queue in transactions'
    print 'graph_args --base 1000 -l 0'
    print 'graph_scale no'
    print 'graph_vlabel Transactions'
    print 'graph_category disk'
    print 'graph_info This graph shows transactions in queue'
    print 'graph_order',
    data = a.parse_iostat()
    for disk in data.keys():
        print ' %s_wait' % (disk),
    print

    for disk in data.keys():
        print '%s_wait.label %s' % (disk, disk)
        print '%s_wait.type DERIVE' % disk
        print '%s_wait.min 0' % disk
        print '%s_wait.draw LINE1' % disk

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        configure()
        sys.exit(0)
    
    get_data()
