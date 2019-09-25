Lab3controller.py is a firewall program that acts as a controller for a switch.
 This controller regulates traffic flow for ARP, ICMP and TCP packets. 

For each type of packet, I defined a match and action to establish a rule. 
I then set my data attribute for the op_flow_mod in order to install my rule into the switch. 
My rule allows packet traffic to flow through. 


Only TCP packets are allowed to flow between h1 and h3 hosts. Any other types of packets that want to flow betweeen h1 and h3 are dropped. I implemented this using the ofp_flow_mod() class for table modification.

To regulate TCP traffic, I checked the IP destination ID and source ID in the ipv4 value. Only TCP packets are allowed to flow between h1 and h3 hosts. All other types of packets are sent as messages that do not contain any data. This stops ARP, ICMP, and other traffic. 

All other traffic that has ICMP or ARP and is NOT flowing between h1 and h3 is flooded out all other ports. 

Any traffic that is not TCP, ICMP, or, ARP is dropped. 