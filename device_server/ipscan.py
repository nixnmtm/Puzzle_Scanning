
import ipaddress
from subprocess import Popen, PIPE
import timeit
import multiprocessing


def ipscan(ip):
    ip = str(ip)
    toping = Popen(["ping", "-c1", "-n", "-i0.1", "-W1", ip], stdout=PIPE)
    output = toping.communicate()[0]
    hostalive = toping.returncode
    if hostalive ==0:
        print("{} is reachable".format(ip))
    # else:
    #     pass
    #     #print("{} is unreachable".format(ip))

def ipdomain(ip="", cidr=int, ipstart="", ipend=""):
    if ip and cidr:
        ip_cidr = str(ip) + "/" + str(cidr)
        iprange = ipaddress.ip_network(ip_cidr)
        iprange = iprange.hosts()
    if ipstart and ipend:
        iplist = ipaddress.summarize_address_range(ipaddress.IPv4Address(ipstart),
                                                   ipaddress.IPv4Address(ipend))
        for i in iplist:
            print(i)
            print(i.hosts())
    return iprange

if __name__ == '__main__':
    ip = "10.10.70.0"
    cidr = 24
    #network = ipdomain(ipstart="10.10.70.1", ipend="10.10.70.10")
    network = ipdomain(ip="10.10.70.0", cidr=24)
    start_time = timeit.default_timer()
    p = multiprocessing.Pool()
    p.map(ipscan, network)
    elapsed = timeit.default_timer() - start_time
    print(elapsed)