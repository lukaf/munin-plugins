import subprocess as sub
import gevent
import sys
import os

timeout = int(os.environ.get('timeout', 5))
hosts = os.environ.get('hosts', '127.0.0.1').split()
ping_cmd = os.environ.get('ping_cmd', 'ping -c1 -W2')

fs = lambda x: x.replace('.', '_')


def pinger(h):
    p = sub.Popen(ping_cmd.split() + [h], stdout=sub.PIPE, stderr=sub.STDOUT)
    p.wait()
    return (h, p.returncode)


def configure():
    print "graph_title Host availability"
    print "graph_args --base 1000 -l 0"
    print "graph_category network"
    for host in hosts:
        print "%s.label %s" % (fs(host), host)
        print "%s.critical 0:0" % fs(host)
        print "%s.type ABSOLUTE" % fs(host)


def get_data():
    workers = [gevent.spawn(pinger, h) for h in hosts]
    gevent.joinall(workers)
    for worker in workers:
        print "%s.value %d" % (worker.value[0].replace('.', '_'),
            worker.value[1])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        configure()
    else:
        get_data()
