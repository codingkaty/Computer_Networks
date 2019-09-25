

This Final Project is a program that represents a network I made, with the help of the TAs in Computer Networks, that is based off of a topology given to me in class.  

It follows the following rules:

1. The trusted and untrusted host can communicate with one another. 

2. No IP traffic can be sent to the server from the untrusted host.

3.The untrusted host can not send any ICMP traffic to host 10, 20, and 30. 

4. The trusted host can communicate with anything in the network. 



I implemented this by using the server_id parameter to  check which server the packet was at. 
Then I sent the packet to a particular port number based on the destination ip address of the packet. 
I dropped the packet if it broke any of the rules listed above.