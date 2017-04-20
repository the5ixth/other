from scapy.all import *
import threading
import multiprocessing
import ipcalc
import logging
import time


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
        self.current = None

    #add host menu items

    def add_host(self, ip, test=False):
        i = Host(ip)
        if test:
            if i.up:
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

    # drop host menu items

    def drop_host(self, host):
        self.hostlist.remove(host)
    
    def drop_down(self):
        self.hostlist = list(set(self.hostlist) - set([h for h in self.hostlist if not h.up]))

    # scan host menu items

    def scan_host(self, host, tpe="well_known"):
        h = self.hostlist.pop(self.hostlist.index(host))
        h.port_scan(tpe)
        time.sleep(20)
        self.hostlist.append(h)
    
    def scan_all(self, tpe="quick"):
        for i in self.hostlist:
            t = threading.Thread(target=i.port_scan, args=(tpe,))
            t.start()

    # show info menu Items 

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
    
    # cli use

    def get_host(self, iput):
        ''' Takes either the IP address or the ID and returns the host object '''
        for i in self.hostlist:
            if i.id == iput:
                return i
            elif i.ip == iput:
                return i

    def main_menu(self):
        print "# Netscan.py #"
        print "1. Add hosts"
        print "2. Set current host( {} )".format(self.current)
        print "3. list hosts"
        print "4. Scan hosts"
        print "5. Delete hosts"
        print "6. Change current host"
        print "7. Exit"
        i = int(raw_input(">>: "))
        print i
        if i == 1:
            self.add_menu()
        elif i == 2:
            self.cur_host_menu()
        elif i == 3:
            self.list_menu()
        elif i == 4:
            self.scan_menu()
        elif i == 5:
            self.delete_menu()
        elif i == 6:
            self.cur_host_menu(True)
        elif i == 7:
            exit(1)


    def add_menu(self):
        print "# Add a host #"
        print "1. Add a single host"
        print "2. Add a Network"
        print "3. Scan a network and add only hosts that are up"
        print "0. Return to main menu"
        i = int(raw_input(">>: "))
        if i == 1:
            print "Enter the IPv4 address"
            ip = raw_input(">>: ")
            self.add_host(ip)
        elif i == 2:
            print "Enter the Network address"
            ip = raw_input('>>: ')
            print "Enter the cidr"
            cdr = raw_input('>>: ')
            self.add_net(ip, cdr)
        elif i == 3:
            print "Enter the Network address"
            ip = raw_input('>>: ')
            print "Enter the cidr"
            cdr = raw_input('>>: ')
            self.scan_net(ip, cdr)
        self.main_menu()

    def cur_host_menu(self, reset=False):
        if self.current is None or reset:
            print "# Set a host as your curent Host #"
            self.show_all(False)
            print "Enter the host ip or name"
            i = raw_input(">>: ")
            self.current = self.get_host(i)
        print "1. Port scan current host"
        print "2. Current host info"
        self.main_menu()
        
    
    def scan_menu(self):
        print "# Port Scanning #"
        print "1. Scan current Host"
        print "2. Scan a Host"
        print "3. Scan all Hosts"
        print "0. Return to main menu"
        i = int(raw_input(">>: "))
        if i == 1:
            self.scan_host(self.current)
        elif i == 2:
            print "Enter the host name or ip to scan"
            addr = raw_input(">>: ")
            self.scan_host(self, self.get_host(addr))
        elif i == 3:
            self.scan_all()
        self.main_menu()

    def delete_menu(self):
        print "# Delete Menu #"
        print "1. Delete Down Hosts"
        print "2. Delete all hosts"
        print "3. Delete single host"
        print "0. Return to main menu"
        i = int(raw_input(">>: "))
        if i == 1:
            self.drop_down()
        elif i == 2:
            self.hostlist = []
        elif i == 3:
            print "Enter the name or address to delete"
            addr = raw_input(">>: ")
            self.drop_host(self.get_host(addr))
        self.main_menu()
    
    def list_menu(self):
        print "# Listing menu #"
        print "1. List all"
        print "2. List hosts that are up"
        print "3. List single host info"
        print "0. Return to main menu"
        i = int(raw_input(">>: "))
        if i == 1:
            self.show_all()
        elif i == 2:
            self.show_up()
        elif i == 3:
            print "Enter the name or address to show info"
            addr = raw_input(">>: ")
            self.show_info(self.get_host(addr))
        self.main_menu()
          
            


m = Menu()

        
import pdir as dir
if __name__  == "__main__":
    m.main_menu()
