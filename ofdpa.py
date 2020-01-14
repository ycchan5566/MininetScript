import os
import sys

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController, Host, OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info, warn

class MyTopo(Topo):

    switch = []
    host = []

    def __init__(self):

        # initialize topology
        Topo.__init__(self)

        for i in range(1, 6):
            self.switch.append(self.addSwitch("s"+str(i), dpid="000000000000000"+str(i)))

        self.host.append(self.addHost("h1", cls=IpHost, mac="00:00:00:00:00:01", ip="10.0.0.1/24", gateway="10.0.0.254"))
        self.host.append(self.addHost("h2", cls=IpHost, mac="00:00:00:00:00:02", ip="10.0.0.2/24", gateway="10.0.0.254"))
        self.host.append(self.addHost("h3", cls=IpHost, mac="00:00:00:00:00:03", ip="10.0.0.3/24", gateway="10.0.0.254"))
        self.host.append(self.addHost("h4", cls=IpHost, mac="00:00:00:00:00:04", ip="10.0.0.4/24", gateway="10.0.0.254"))
        self.host.append(self.addHost("h5", cls=IpHost, mac="00:00:00:00:00:05", ip="10.0.0.5/24", gateway="10.0.0.254"))

        # add links
	for i in range(5):
          self.addLink(self.switch[i], self.host[i])

        self.addLink(self.switch[1], self.switch[0])
        self.addLink(self.switch[1], self.switch[2])
        self.addLink(self.switch[1], self.switch[3])
        self.addLink(self.switch[2], self.switch[4])
        self.addLink(self.switch[3], self.switch[4])

class IpHost(Host):
    def __init__(self, name, gateway, *args, **kwargs):
        super(IpHost, self).__init__(name,*args,**kwargs)
        self.gateway = gateway

    def config(self, **kwargs):
        Host.config(self,**kwargs)
        mtu = "ifconfig " + self.name + "-eth0 mtu 1490"
        self.cmd(mtu)
        self.cmd('ip route add default via %s' % self.gateway)

topos = {'mytopo': (lambda: MyTopo())}

if __name__ == "__main__":
    setLogLevel('info')

    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.addController('c0', switch=OVSSwitch, controller=RemoteController, ip="127.0.0.1")

    net.start()
    CLI(net)
    net.stop()
