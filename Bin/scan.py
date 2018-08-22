from scapy.all import *
import socket
from os import system

closed = 0x14  # tcp flag key for closed port

conf.verb = 0  # stop scapy from printing


def normal_scan(ip, start, end):
    """
    scans through all the requested ports
    :param ip: requested ip
    :param start: first port
    :param end: last port
    :return: scan results
    """
    ports = []
    for x in xrange(start, end):
        s = socket.socket()
        s.settimeout(0.05)  # set a timeout of 0.01 second to avoid delays

        if not s.connect_ex((ip, x)):  # connect_ex returns 0 if it managed to connect
            s.close()
            ports.append(x)

        s.close()

    return ports


def host_up(ip):
    """
    checks if the host is up
    :param ip: requested ip
    :return: True if the host is up otherwise False
    """
    ping = sr1(IP(dst=ip) / ICMP(), timeout=3)

    if ping:
        return True
    return False


def stealth_scan(ip, start, end):
    """
    scans through all the requested ports in a stealthy way
    :param ip: requested ip
    :param start: first port
    :param end: last port
    :return: scan results
    """
    ans, _ = sr(IP(dst=ip) / TCP(sport=RandShort(), dport=xrange(start, end), flags='S'), timeout=12)  # send syn packet

    ports = []
    for x in ans:
        if x:
            if x[1][TCP].flags != closed:  # check if the flag of the returning packet say its closed
                send(IP(dst=ip) / TCP(sport=RandShort(), dport=x[1][TCP].sport, flags='R'))  # close the connection
                ports.append(x[1][TCP].sport)

    return ports


def get_host_name(ip):
    """
    Finds the host name for a given host ip
    :param ip: requested ip
    :return: host name if found
    """
    if socket.getfqdn(ip)[:-6] == socket.getfqdn():  # checks i
        return socket.getfqdn()
    return socket.getfqdn(ip)


def check_port(port):
    """
    check if the port is valid
    :param port: a string to check
    :return: True if the string is a valid port otherwise False
    """
    if port.isdigit():
        if 65536 > int(port) > 0:
            return True
    return False
