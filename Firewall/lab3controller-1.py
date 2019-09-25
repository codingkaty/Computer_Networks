# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

# This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.

    check_icmp = packet.find('icmp')
    check_arp = packet.find('arp')
    check_tcp = packet.find('tcp')

    if check_arp is not None:
      msg = of.ofp_flow_mod() 
      msg.match = of.ofp_match.from_packet(packet)
      #msg.match.dl_type = 0x806
      msg.data = packet_in

      #set action
      action = of.ofp_action_output(port = of.OFPP_FLOOD)
      msg.actions.append(action)
     # msg.data = packet_in
      self.connection.send(msg)
      print ('arp found!')

    elif check_icmp is not None:
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.data = packet_in
     # msg.match.dl_type = 0x800

      action = of.ofp_action_output(port = of.OFPP_FLOOD)
      msg.actions.append(action)
      self.connection.send(msg)

      print('icmp found!')

    elif check_tcp is not None:
     # msg.match = of.ofp_match.from_packet(packet)     
    #  print('TCP DOOUND!!')
      
     msg = of.ofp_flow_mod()
     # msg.match.nw_proto = 6
     msg.match = of.ofp_match.from_packet(packet)
     msg.data = packet_in
     print('got here!')
     ipv4 = packet.find('ipv4')
     print (ipv4.srcip)

     if ipv4.srcip == '10.0.1.10' and ipv4.dstip == '10.0.1.30':
       # msg = of.ofp_flow_mod()
       # msg.match = of.ofp_match.from_packet(packet)
       # msg.data = packet_in

       action = of.ofp_action_output(port = of.OFPP_FLOOD)
       msg.actions.append(action)
       self.connection.send(msg)
       print('h1 found!')

     elif ipv4.srcip == '10.0.1.30' and ipv4.dstip == '10.0.1.10':
       action = of.ofp_action_output(port = of.OFPP_FLOOD)
       msg.actions.append(action)
       self.connection.send(msg)
       print('h1 found!')

     else:
       self.connection.send(msg)
       print('h4 is found')     

   # print('example found!!')


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)

