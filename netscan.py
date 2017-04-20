from scapy.all import *
import threading
import multiprocessing
import ipcalc
import logging


logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class Host():

    def __init__(self, ip, name=None):
        if name is None:
            self.id = ip
        else:
            self.id = name
        self.ip = ip
        self.ports = []
        self.mac = ''
        self.up = False
        self.is_up()
        self.get_mac()

    def __repr__(self):
        return self.id

    def set_id(self, name):
        self.id = name
    
    def is_up(self):
        resp, unans = sr(IP(dst=self.ip)/ICMP(), timeout=1, retry=3, verbose=0)
        for s, r in resp:
            if r[ICMP].type == 0:
                self.up = True
            else:
                self.up = False

    def get_mac(self):
        resp, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=self.ip), timeout=1, retry=3, verbose=0)
        for s, r in resp:
            self.mac = r[Ether].src

    def port_scan(self, tpe="well_known", port=80):
        options = {'well_known': (1, 1024),
                   'all': (1,65534),
                   'quick': (1, 500),
                   'single': port}

        if tpe == "single":
            self.port(port)
        else:
            f, l = options[tpe]
            for i in range(f, l):
                self.ports = []
                t = threading.Thread(target=self.port, args=(i,))
                t.start()

    def port(self, port, tpe='syn'):
        options = {'syn': (2, 18),
                   'xmas': (41, 0)}
 
        resp, unans = sr(IP(dst=self.ip)/TCP(dport=port, flags=2), timeout=1, retry=3, verbose=0)
        for s, r in resp:
            if r[TCP].flags == 18:
                self.ports.append(port)

    def show_ports(self, banner=True):
        if banner:
            print "[X] Open ports for host {} [X]".format(self.ip)
        for i in self.ports:
            print " [+] {}".format(i)
      
    def show_info(self):
        print "---------------------------------"
        print "[] IP: {} ".format(self.ip)
        print "[] MAC: {} ".format(self.mac)
        if self.up:
            print "[] Host is UP."
        else:
            print "[] Host is DOWN."
        self.show_ports()
        print "---------------------------------"
        

class Menu():
    def __init__(self):
        self.hostlist = []
        
    def add_host(self, ip, test=False):
        i = Host(ip)
        if test and i.up:
            self.hostlist.append(i)
        else:
            self.hostlist.append(i)

    def add_net(self, network, cidr=24, scan=False):
        ''' Add a network to your hostlist without scanning'''
        self.scan_net(network, cidr, scan)

    def scan_net(self, network, cidr=24, scan=True):
        ''' Add hosts within a defined network that are up to your hostlist'''
        s = network + "/" + str(cidr)
        for i in ipcalc.Network(s):
            t = threading.Thread(target=self.add_host, args=(str(i), scan, ))
            t.start()

    def drop_host(self, host):
        self.hostlist.remove(host)
    
    def drop_down(self):
        self.hostlist = list(set(self.hostlist) - set([h for h in self.hostlist if not h.up]))

    
    def scan_host(self, host, tpe="well_known"):
        host.port_scan(tpe)
    
    def scan_all(self, tpe="quick"):
        for i in self.hostlist:
            p = multiprocessing.Process(target=i.port_scan, args=(tpe,))
            p.start()

    def show_host(self, host):
        ''' Display all the info for a particular host'''
        host.print_info()
   
    def show_all(self, verbose=True):
        '''Display all of the hosts in the hostlist'''
        for i in self.hostlist:
            if verbose:
                i.show_info()
            else:
                print i.id

    def show_up(self, verbose=True):
        ''' Shows only the hosts that are up'''
        for i in self.hostlist:
            if i.up:
                if verbose:
                    i.show_info()
                else:
                    print "[] {}".format(i.ip)

    def get_host(self, iput):
        ''' Takes either the IP address or the ID and returns the host object '''
        for i in self.hostlist:
            if i.id == iput:
                return i
            elif i.ip == iput:
                return i

    def banner(self):
        print "soon"


m = Menu()

m.add_net('10.0.2.1', 28)
print "===Starting==="
        
import pdir as dir

