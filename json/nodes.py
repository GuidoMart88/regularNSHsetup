#!/usr/bin/python
from configuration import *
import argparse
import requests,json
from requests.auth import HTTPBasicAuth
from subprocess import call
import time
import sys
import os


def put(host, port, uri, data, debug=False):
    '''Perform a PUT rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri

    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "PUT %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.put(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)

def post(host, port, uri, data, debug=False):
    '''Perform a POST rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri
    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "POST %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)

def delete(host, port, uri):
    url='http://'+host+":"+port+uri
    r = requests.delete(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    #r.raise_for_status()

def get_service_nodes_uri():
    return "/restconf/config/service-node:service-nodes"

def get_service_nodes_data():
    return {
    "service-nodes": {
        "service-node": [
            {
                "name": "classifier1",
                "service-function": [
                ],
                "ip-mgmt-address": classifier1
            },                        
            {
                "name": "SFF1",
                "service-function": [
                ],
                "ip-mgmt-address": sff1
            },
            {
                "name": "sf1",
                "service-function": [
                    "sf1"
                ],
                "ip-mgmt-address": firewall
            },
            {
                "name": "sf2",
                "service-function": [
                    "sf2"
                ],
                "ip-mgmt-address": firewall2
            },
            {
                "name": "sf3",
                "service-function": [
                    "sf3"
                ],
                "ip-mgmt-address": dpi
            },
			{
                "name": "sf4",
                "service-function": [
                    "sf4"
                ],
                "ip-mgmt-address": dpi2
            }
			
        ]
    }
}

def get_service_functions_uri():
    return "/restconf/config/service-function:service-functions"

def get_service_functions_data():
    return {
    "service-functions": {
        "service-function": [
            {
                "name": "sf1",
                "type": "firewall",
                "ip-mgmt-address": firewall,
                "sf-data-plane-locator": [
                    {
                        "name": "sf1-dpl",
                        "port": 6633,
                        "ip": firewall,
                        "transport": "service-locator:vxlan-gpe",
                        "service-function-forwarder": "sff1"
                    }
                ],
                "rest-uri": "http://"+firewall+":5000"
            },
			{
                "name": "sf2",
                "type": "firewall",
                "ip-mgmt-address": firewall2,
                "sf-data-plane-locator": [
                    {
                        "name": "sf2-dpl",
                        "port": 6633,
                        "ip": firewall2,
                        "transport": "service-locator:vxlan-gpe",
                        "service-function-forwarder": "sff1"
                    }
                ],
                "rest-uri": "http://"+firewall2+":5000"
            },
            {
                "name": "sf3",
                "type": "dpi",
                "ip-mgmt-address": dpi,
                "sf-data-plane-locator": [
                    {
                        "name": "sf3-dpl",
                        "port": 6633,
                        "ip": dpi,
                        "transport": "service-locator:vxlan-gpe",
                        "service-function-forwarder": "sff1"
                    }
                ],
                "rest-uri": "http://"+dpi+":5000"
            },
			{
                "name": "sf4",
                "type": "dpi",
                "ip-mgmt-address": dpi2,
                "sf-data-plane-locator": [
                    {
                        "name": "sf4-dpl",
                        "port": 6633,
                        "ip": dpi2,
                        "transport": "service-locator:vxlan-gpe",
                        "service-function-forwarder": "sff1"
                    }
                ],
                "rest-uri": "http://"+dpi2+":5000"
            }
         
        ]
    }
}

def get_service_function_forwarders_uri():
    return "/restconf/config/service-function-forwarder:service-function-forwarders"

def get_service_function_forwarders_data():
    return {
    "service-function-forwarders": {
        "service-function-forwarder": [  
        {
            "name": "sff1",
            "service-node": "SFF1",
            "ip-mgmt-address": sff1,
            
            "service-function-forwarder-ovs:ovs-bridge": {
                    "bridge-name": "br-sfc",
            },
             "sff-data-plane-locator": [
                    {
                        "name": "sff1-dpl",
                        "data-plane-locator": {
                            "transport": "service-locator:vxlan-gpe",
                            "port": 6633,
                            "ip": sff1
                        },
                        "service-function-forwarder-ovs:ovs-options": {
                            "remote-ip": "flow",
                            "dst-port": "6633",
                            "key": "flow",
                            "exts": "gpe",
                            "nsp": "flow",
                            "nsi": "flow",
                            "nshc1": "flow",
                            "nshc2": "flow",
                            "nshc3": "flow",
                            "nshc4": "flow"
                        }
                    }
                ],
            "service-function-dictionary": [
                    {
                        "name": "sf1",
                        "sff-sf-data-plane-locator": {
                             "sf-dpl-name": "sf1-dpl",
                             "sff-dpl-name": "sff1-dpl"
                        }
                    },
                    {
                        "name": "sf2",
                        "sff-sf-data-plane-locator": {
                             "sf-dpl-name": "sf2-dpl",
                             "sff-dpl-name": "sff1-dpl"
                        }
                    },
                    {
                        "name": "sf3",
                        "sff-sf-data-plane-locator": {
                             "sf-dpl-name": "sf3-dpl",
                             "sff-dpl-name": "sff1-dpl"
                        }
                    },
					{
                        "name": "sf4",
                        "sff-sf-data-plane-locator": {
                             "sf-dpl-name": "sf4-dpl",
                             "sff-dpl-name": "sff1-dpl"
                        }
                    }
                ]
        }
        ]
    }
}


if __name__ == "__main__":

    print "deleting service function forwarders"
    delete(controller, DEFAULT_PORT, get_service_function_forwarders_uri())
    time.sleep(1)
    print "deleting service functions"
    delete(controller, DEFAULT_PORT, get_service_functions_uri())
    time.sleep(1)
    print "deleting service nodes"
    delete(controller, DEFAULT_PORT, get_service_nodes_uri())

    print "sending service nodes"
    put(controller, DEFAULT_PORT, get_service_nodes_uri(), get_service_nodes_data(), True)
    print "sending service functions"
    put(controller, DEFAULT_PORT, get_service_functions_uri(), get_service_functions_data(), True)
    print "sending service function forwarders"
    put(controller, DEFAULT_PORT, get_service_function_forwarders_uri(), get_service_function_forwarders_data(), True)
