from PySide import QtCore
from scapy.all import *
from math import log
from threading import Thread
from time import sleep, clock
from cPickle import dumps
import requests


class Scan(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.not_found = '\x07rfc1918\x07leakage\x00\x04stop\xc0J\x00\x00\x00\x01\x00\x00\x0e\x10\x00\x00\x04\xb0\x00' \
                         '\t:\x80\x00\x00*0'  # text that you get when an ip isn't found
        self.mac = ''
        self.gate = ''

        self.ips = []
        self.macs = []

    def __del__(self):
        self.wait()

    @staticmethod
    def reverse_ip(ip):
        """
        reverses target ip
        :param ip: target ip
        :return: reversed ip
        """
        i = ip.split('.')
        i.reverse()
        return '.'.join(i)

    def resolve_name(self, ip):
        """
        :param ip: target ip address
        :return: hostname if found
        """
        p = sr1(IP(dst=self.gate) / UDP() / DNS(rd=1, qd=DNSQR(
            qname="{}.in-addr.arpa".format(self.reverse_ip(ip)), qtype='PTR')), timeout=0.2)

        if p:
            if 'DNSRR' in p:
                if p['DNSRR'].rdata != self.not_found:
                    return p['DNSRR'].rdata[:-1]

        try:
            return socket.gethostbyaddr(ip)[0]

        except socket.herror:
            return 'n\\a'

    @staticmethod
    def get_gate():
        """
        gets the the gateaway for the selected iface
        :return: gw if found
        """
        pkt = sr1(IP(dst='www.google.co.il', ttl=1) / ICMP(), timeout=0.2, retry=2)
        if pkt:
            return pkt.src

        return ''

    @staticmethod
    def get_ven(mac):
        """
        :param mac: target mac address
        :return: vendor if found
        """
        try:
            a = requests.get('http://macvendors.co/api/{}/pipe'.format(mac))
            if a.text == 'Vendor not found\n':
                return 'n\\s'

            return a.text.split('|')[0].replace('"', '')

        except requests.exceptions.ConnectionError:
            return 'n\\a'

    def check(self, mac):
        """
        checks that the ip or mac aren't discovered already
        :param mac: target mac address
        :return: True if wasn't discovered otherwise False
        """
        if mac not in self.macs:
            self.macs.append(mac)
            return True

        return False

    @staticmethod
    def mask(bytes_network, bytes_mask):
        """
        calculates the network address and mask
        :param bytes_network: network address in bytes
        :param bytes_mask: network mask in bytes
        :return: network address / mask
        """
        if bytes_mask <= 0 or bytes_mask >= 0xFFFFFFFF:
            raise ValueError("illegal netmask value", hex(bytes_mask))

        network = utils.ltoa(bytes_network)  # calculate the network address
        netmask = 32 - int(round(log(0xFFFFFFFF - bytes_mask, 2)))  # calculate the mask range

        if netmask < 16:  # nets that have a mask bigger than that aren't supported
            return None

        return '{}/{}'.format(network, netmask)

    @staticmethod
    def ping(ip):
        """
        pings the target ip
        :param ip: target ip
        :return: ping timeout
        """
        st = clock()
        ans = sr1(IP(dst=ip) / ICMP(), timeout=0.5)

        if ans:
            return '{}ms'.format(int((clock() - st) * 100)), ans[IP].ttl

        return 'n\\a', None

    def detect_os(self, ip):
        """
        detects the os and ping timeout
        :param ip: target ip
        :return: os and ping
        """
        sc, ttl = self.ping(ip)

        if not ttl:
            methods = (IP(dst=ip) / UDP(sport=161) / SNMP(community="private", PDU=SNMPset(
                varbindlist=SNMPvarbind(oid=ASN1_OID("1.3.6.1.4.1.9.2.1.55.192.168.30.10"),
                                        value="pwnd-router.config"))),
                       IP(dst=ip) / UDP(sport=1900, dport=1900) / Raw(
                           load="M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "
                                "\"ssdp:discover\"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n"))
            for meth in methods:
                ans = sr1(meth, timeout=0.5)
                if ans:
                    ttl = ans[IP].ttl
                    break

        if ttl:
            if ttl == 64:
                return 'Linux', sc

            elif ttl == 128:
                return 'Windows', sc

            else:
                print '{}/{}'.format(ip, ttl)
                return 'n\\a', sc

        return 'n\\a', 'n\\a'

    def analayzer(self, ip, mac):
        """
        analyze the given parmaters and sends to gui
        :param ip: target ip
        :param mac: target mac
        :return: True if it's not in the table already otherwise false
        """

        if self.check(mac):

            ven = self.get_ven(mac)

            if ip == conf.iface.ip:
                nam = socket.gethostname()  # or platform.node()
                system = platform.system()
                ping = 'n\\a'

            else:
                nam = self.resolve_name(ip)

                system, ping = self.detect_os(ip)

                if 'android' in nam:
                    system = 'Android'

                elif 'Apple' in ven:  # need some rework
                    system = 'iOS'

            self.emit(QtCore.SIGNAL('device(QString)'),
                      dumps(['Online', ip, nam, mac, ven, system, ping]))

            if ip != conf.iface.ip:
                return True

            return False

    def get_net(self):
        """
        :return: broadcast address
        """
        if conf.iface.ip == '0.0.0.0' or not self.gate:
            raise TypeError

        for x in scapy.config.conf.route.routes:
            try:
                if conf.iface in x:
                    net = self.mask(x[0], x[1])
                    if net:
                        return net

            except Exception as er:
                if type(er) == ValueError:
                    continue

                print '{} ({})'.format(er, type(er))

    def initial_scan(self):
        """
        scans for all online hosts on the current iface
        """
        self.emit(QtCore.SIGNAL('status(QString)'), 'Initial scan has been activated')
        try:
            net = self.get_net()

            if not net:
                raise TypeError

            ans, _ = arping(net, retry=2, timeout=0.5)

        except TypeError:
            self.emit(QtCore.SIGNAL('error()'))
            return

        self.emit(QtCore.SIGNAL('prog(int)'), len(ans))

        for x in ans:
            ip = x[1].psrc
            mac = x[1].src

            if self.analayzer(ip, mac):
                pass

            self.emit(QtCore.SIGNAL('prog(int)'), 1)

        self.emit(QtCore.SIGNAL('prog(int)'), 0)

    def fil(self, p):
        """
        checks if a new host has joined the network
        :param p: sniffed packet
        """
        if 'BOOTP' in p:
            if p['BOOTP'].yiaddr == '0.0.0.0':
                self.mac = p.src

            elif self.mac:
                ip = p['BOOTP'].yiaddr

                if self.analayzer(ip, self.mac):
                    self.emit(QtCore.SIGNAL('neo(QString, QString)'), ip, 'joined')

                self.mac = ''

    def run(self):
        """
        runs the necessary functions
        """
        try:
            self.gate = self.get_gate()

        except socket.gaierror:
            self.emit(QtCore.SIGNAL('error()'))
            return
        Thread(self.initial_scan()).start()
        self.emit(QtCore.SIGNAL('status(QString)'), 'Scanning for new hosts')
        sniff(lfilter=self.fil)
