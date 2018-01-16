#!/bin/sh

# auto-sff-name means agent will try to discover its SFF name dynamically during
# start-up and later when it receives a RSP request
python3.5 sfc/sfc_agent.py --rest --odl-ip-port 172.17.0.1:8181 --auto-sff-name --debug-level --legacy-vxlan
