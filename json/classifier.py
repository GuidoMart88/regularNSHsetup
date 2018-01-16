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

def delete(host, port, uri):
    url='http://'+host+":"+port+uri
    r = requests.delete(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    #r.raise_for_status()

def get_service_function_classifiers_uri():
    return "/restconf/config/service-function-classifier:service-function-classifiers/"

def get_service_function_classifiers_data():
    return  {
  "service-function-classifiers": {
    "service-function-classifier": [
       {
            "name": "classifier1",
            "acl": {
                "name": "ACL1",
                "type": "ietf-access-control-list:ipv4-acl"
            },
            "scl-service-function-forwarder": [
                {
                    "name": "sff1",
                    "interface": "client"
                }
            ]
        },
        {
            "name": "classifier2",
            "acl": {
                "name": "ACL2",
                "type": "ietf-access-control-list:ipv4-acl"
            },
            "scl-service-function-forwarder": [
                {
                    "name": "sff1",
                    "interface": "service"
                }
            ]
        }
    ]
  }
}

if __name__ == "__main__":

    print "deleting service function classifiers"
    delete(controller, DEFAULT_PORT, get_service_function_classifiers_uri())
    time.sleep(1)

    print "sending service function classifiers"
    put(controller, DEFAULT_PORT, get_service_function_classifiers_uri(), get_service_function_classifiers_data(), True)

