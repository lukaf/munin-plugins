#!/usr/bin/env python
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
    return (h, p)


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
        # wait for Popen
        worker.value[1].wait()
        print "%s.value %d" % (fs(worker.value[0]), worker.value[1].returncode)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        configure()
    else:
        get_data()
