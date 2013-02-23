#!/usr/bin/env python
import subprocess as sub
import Queue
import sys
import os

timeout = int(os.environ.get('timeout', 5))
hosts = os.environ.get('hosts', '127.0.0.1').split()
ping_cmd = os.environ.get('ping_cmd', 'ping -c1 -W2')
q = Queue.Queue()


def fs(x):
    return x.replace('.', '_')


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
    output = []
    for h in hosts:
        q.put(pinger(h))

    while True:
        try:
            #p = q.get(block=False)
            host, p = q.get(block=False)
            if p.poll() is not None:
                output.append("%s.value %d" % (fs(host), p.returncode))
            else:
                q.put((host, p))
            #if p[1].poll() is not None:
            #    output.append(
            #            "%s.value %d" % (fs(p[0]), p[1].returncode)
            #            )
            #else:
            #    q.put(p)
        except Queue.Empty:
            break

    print '\n'.join(output)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        configure()
    else:
        get_data()
