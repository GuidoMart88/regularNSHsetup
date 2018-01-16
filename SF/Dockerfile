FROM ubuntu:latest
RUN apt-get update && apt-get install -y git wget nano net-tools iproute iputils-* libssl-dev openssl libnetfilter-queue-dev python3-flask python3-pip python3-openssl
RUN pip3 install -U  paramiko flask requests netifaces pyopenssl
WORKDIR /home/root
RUN git clone https://github.com/opendaylight/sfc.git
WORKDIR /home/root/sfc
COPY start_agent.sh /home/root/sfc/sfc-py/
WORKDIR /home/root/sfc/sfc-py
