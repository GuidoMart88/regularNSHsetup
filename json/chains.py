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

def get_service_function_chains_uri():
    return "/restconf/config/service-function-chain:service-function-chains/"

def get_service_function_chains_data():
    return {

    "service-function-chains": {
       "service-function-chain": [
            {
                "name": "SFC1",
                "symmetric": "false",
                "sfc-service-function": [
                    {
                       "name": "sf1",
                       "type": "firewall"
                    },
                    {
                       "name": "sf2",
                       "type": "dpi"
                    }
                ]
            }         
        ]
    }
}


def get_service_function_metadata_uri():
    return "/restconf/config/service-function-path-metadata:service-function-metadata/"

def get_service_function_metadata_data():
    return {
  "service-function-metadata": {
    "context-metadata": [
      {
        "name": "NSH1",
        "context-header1": "1",
        "context-header2": "2",
        "context-header3": "3",
        "context-header4": "4"
      }
    ]
  }
}

def get_service_function_paths_uri():
    return "/restconf/config/service-function-path:service-function-paths/"

def get_service_function_paths_data():
    return {
    "service-function-paths": {
        "service-function-path": [
            {
                "name": "SFP1",
                "service-chain-name": "SFC1",
                "starting-index": 255,
                "symmetric": "false",
                "context-metadata": "NSH1",
            }
        ]
    }
}



if __name__ == "__main__":

    print "deleting service function paths"
    delete(controller, DEFAULT_PORT, get_service_function_paths_uri())
    time.sleep(1)
    print "deleting service function metadata"
    delete(controller, DEFAULT_PORT, get_service_function_metadata_uri())
    time.sleep(1)
    print "deleting service function chains"
    delete(controller, DEFAULT_PORT, get_service_function_chains_uri())
    time.sleep(1)

    print "sending service function chains"
    put(controller, DEFAULT_PORT, get_service_function_chains_uri(), get_service_function_chains_data(), True)
    print "sending service function metadata"
    put(controller, DEFAULT_PORT, get_service_function_metadata_uri(), get_service_function_metadata_data(), True)
    print "sending service function paths"
    put(controller, DEFAULT_PORT, get_service_function_paths_uri(), get_service_function_paths_data(), True)
