#!/usr/bin/python
from configuration import *
import argparse
import requests,json
from requests.auth import HTTPBasicAuth
from subprocess import call
import time
import sys
import os


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


def get_rendered_service_path_uri():
    return "/restconf/operations/rendered-service-path:create-rendered-path/"

def get_rendered_service_path_data():
    return {
"input":    {
        "name": "RSP1",
        "parent-service-function-path": "SFP1",
        "symmetric": "false"
    }
    
}

if __name__ == "__main__":

    print "sending rendered service path"
    post(controller, DEFAULT_PORT, get_rendered_service_path_uri(), get_rendered_service_path_data(), True)
