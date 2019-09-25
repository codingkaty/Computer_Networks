#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.0.1.10/24', defaultRoute="h1-eth0")
    h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.0.2.20/24', defaultRoute="h2-eth0")
    h3 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.0.3.30/24', defaultRoute="h3-eth0")
    server = self.addHost('h4',mac='00:00:00:00:00:04',ip='10.0.4.40/24', defaultRoute="h4-eth0")
    t_host = self.addHost('h5',mac='00:00:00:00:00:05',ip='104.82.214.112/24', defaultRoute="h5-eth0")
    ut_host = self.addHost('h6',mac='00:00:00:00:00:06',ip='156.134.2.12/24', defaultRoute="h6-eth0")

    # Create a switch. No changes here from Lab 1.
    floor1 = self.addSwitch('s1')
    floor2 = self.addSwitch('s2')
    floor3 = self.addSwitch('s3')
    core = self.addSwitch('s4')
    data_center = self.addSwitch('s5')
    

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    self.addLink(h1,floor1, port1=0, port2=1)  #connect host 1 and floor 1 switch
    self.addLink(h2,floor2, port1=0, port2=1)  #connect host 2 and floor 2 switch
    self.addLink(h3,floor3, port1=0, port2=1)  #connect host 3 and floor 3 switch
    self.addLink(server,data_center, port1=0, port2=1)  #connect server and data center switch
    self.addLink(t_host, core, port1=0, port2=4) #connect trusted host and core switch
    self.addLink(ut_host, core, port1=0, port2=3) #connect untrusted host and core switch

    #connect all switches to the core switch
    self.addLink(floor1, core, port1=2, port2=7)
    self.addLink(floor2, core, port1=2, port2=6)
    self.addLink(floor3, core, port1=2, port2=5)
    self.addLink(data_center, core, port1=2, port2=8)    

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
