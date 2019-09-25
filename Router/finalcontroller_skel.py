# Final Skeleton
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
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

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    check_arp = packet.find('arp')
    check_icmp = packet.find('icmp')
    check_tcp = packet.find('tcp')


    if check_arp is not None:
      print "packet is arp"
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.data = packet_in

      action = of.ofp_action_output(port = of.OFPP_FLOOD)
      msg.actions.append(action)
      self.connection.send(msg)

    elif check_icmp is not None:
      print "port on switch is: "
      print(port_on_switch)
      print "the switch id is..."
      print(switch_id)
      print "packet is icmp"
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.data = packet_in
      ip = packet.find('ipv4')
      
      if ip.srcip == '156.134.2.12' and ip.dstip == '104.82.214.112':
        action = of.ofp_action_output(port = 4)
        msg.actions.append(action)
        self.connection.send(msg)

      elif ip.srcip == '104.82.214.112' and ip.dstip == '156.134.2.12':
        action = of.ofp_action_output(port = 3)
        msg.actions.append(action)
        self.connection.send(msg)

      elif ip.srcip == '156.134.2.12':
        self.connection.send(msg)
        print('untrusted host blocked on icmp')

      if switch_id == 1:
        print "floor 1"
          
        if ip.srcip == "10.0.1.10": #h1 is sending a packet
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          self.connection.send(msg)

        elif ip.dstip == "10.0.1.10": #h1 is receiving a packet
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          self.connection.send(msg)


      elif switch_id == 2:
        print "floor 2"
        if ip.srcip == "10.0.2.20": #if h2 is sending a packet
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          self.connection.send(msg)

        elif ip.dstip == "10.0.2.20": #if h2 is receiving a packet
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          self.connection.send(msg)
        

      elif switch_id == 3:
        print "floor 3"
        if ip.srcip == "10.0.3.30": #if h3 is sending a packet
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          self.connection.send(msg)

        elif ip.dstip == "10.0.3.30": #if h3 is receiving a packet
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          self.connection.send(msg)


      elif switch_id == 5:
        print "data center"
        if ip.srcip == "10.0.4.40": #if h4 is sending a packet
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          self.connection.send(msg)

        elif ip.dstip == "10.0.4.40": #if h4 is receiving a packet
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          self.connection.send(msg)


      elif switch_id == 4:
        print "core"
        if ip.dstip == "10.0.1.10": #h1
          action = of.ofp_action_output(port = 7)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "10.0.2.20": #h2
          action = of.ofp_action_output(port = 6)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "10.0.3.30": #h3
          action = of.ofp_action_output(port = 5)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "10.0.4.40": #h4
          action = of.ofp_action_output(port = 8)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "104.82.214.112": #trusted host
          action = of.ofp_action_output(port = 4)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "156.134.2.12": #untrusted host
          action = of.ofp_action_output(port = 3)
          msg.actions.append(action)
          self.connection.send(msg)

          

    elif check_tcp is not None:
      print ("packet is tcp!!!")
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.data = packet_in
      ip = packet.find('ipv4')

      if ip.srcip == '156.134.2.12/24' and ip.dstip == '10.0.4.40/24':
        self.connection.send(msg)
        print"communication betweeen untrusted host & server blocked"


      if switch_id == 1:
        print "floor 1"
          
        if ip.srcip == "10.0.1.10": #h1 is sending a packet
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          self.connection.send(msg)

        elif ip.dstip == "10.0.1.10": #h1 is receiving a packet
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          self.connection.send(msg)


      elif switch_id == 2:
        print "floor 2"
        if ip.srcip == "10.0.2.20": #if h2 is sending a packet
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          self.connection.send(msg)

        elif ip.dstip == "10.0.2.20": #if h2 is receiving a packet
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          self.connection.send(msg)
        

      elif switch_id == 3:
        print "floor 3"
        if ip.srcip == "10.0.3.30": #if h3 is sending a packet
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          self.connection.send(msg)

        elif ip.dstip == "10.0.3.30": #if h3 is receiving a packet
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          self.connection.send(msg)


      elif switch_id == 5:
        print "data center"
        if ip.srcip == "10.0.4.40": #if h4 is sending a packet
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          self.connection.send(msg)

        elif ip.dstip == "10.0.4.40": #if h4 is receiving a packet
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          self.connection.send(msg)


      elif switch_id == 4:
        print "core"
        if ip.dstip == "10.0.1.10": #h1
          action = of.ofp_action_output(port = 7)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "10.0.2.20": #h2
          action = of.ofp_action_output(port = 6)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "10.0.3.30": #h3
          action = of.ofp_action_output(port = 5)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "10.0.4.40": #h4
          action = of.ofp_action_output(port = 8)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "104.82.214.112": #trusted host
          action = of.ofp_action_output(port = 4)
          msg.actions.append(action)
          self.connection.send(msg)
        if ip.dstip == "156.134.2.12": #untrusted host
          action = of.ofp_action_output(port = 3)
          msg.actions.append(action)
          self.connection.send(msg)
      
    print "Hello, World!"

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
