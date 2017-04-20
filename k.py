import time
import socket
import sys

while True:
    print 'trying'
    try:
        s = socket.socket()
        e = socket.socket()
        n = socket.socket()


        me = '127.0.0.1'
        s.connect((me, 7000))
        time.sleep(1)
        print 'got 7'
        e.connect((me, 8000))
        time.sleep(1)
        print 'got 8'
        n.connect((me, 9000))
        print 'success'
        print "terminal open at: {}".format(me)
        while True:
            try:
                cmd = raw_input('>>:')
                n.send('f' + cmd)
                try:
                    ret = n.recv(10240)
                except KeyboardInterrupt:
                    pass
                print ret
            except KeyboardInterrupt:
                exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except socket.error:
        time.sleep(1)
        pass
