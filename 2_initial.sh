#!/bin/bash
sudo ovs-vsctl del-br br-sfc
sudo ovs-vsctl add-br br-sfc
sudo ovs-vsctl set-manager tcp:10.0.2.15:6640
sudo ovs-vsctl set-controller br-sfc tcp:10.0.2.15:6653
docker stop client SF1 SF2 SF3 SF4 SF5 SF6 service
docker rm client SF1 SF2 SF3 SF4 SF5 SF6 service

docker run -itd --name client  cnnet-sf "/bin/bash"
docker run -itd --name SF1  cnnet-sf "/bin/bash"
docker run -itd --name SF2  cnnet-sf "/bin/bash"
docker run -itd --name SF3  cnnet-sf "/bin/bash"
docker run -itd --name SF4  cnnet-sf "/bin/bash"
docker run -itd --name SF5  cnnet-sf "/bin/bash"
docker run -itd --name SF6  cnnet-sf "/bin/bash"
docker run -itd --name service  cnnet-sf "/bin/bash" 

docker start client SF1 SF2 SF3 SF4 SF5 SF6 service

sudo ./pipework br-sfc -l client client 192.168.3.2/24
sudo ./pipework br-sfc -l SF1 SF1  192.168.3.3/24
sudo ./pipework br-sfc -l SF2 SF2  192.168.3.4/24
sudo ./pipework br-sfc -l SF3 SF3  192.168.3.5/24
sudo ./pipework br-sfc -l SF4 SF4  192.168.3.6/24
sudo ./pipework br-sfc -l service service  192.168.3.7/24

sudo ovs-ofctl add-flow br-sfc priority=100,in_port=1,arp,actions=output:6
sudo ovs-ofctl add-flow br-sfc priority=100,in_port=6,arp,actions=output:1
sudo ovs-ofctl add-flow br-sfc priority=100,in_port=6,icmp,actions=output:1

