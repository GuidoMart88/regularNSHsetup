#!/usr/bin/python
from configuration import *
import argparse
import requests,json
from requests.auth import HTTPBasicAuth
from subprocess import call
import time
import sys
import os


def delete(host, port, uri):
    url='http://'+host+":"+port+uri
    r = requests.delete(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    #r.raise_for_status()

def get_rendered_service_path_uri():
    return "/restconf/operations/rendered-service-path:create-rendered-path/"

if __name__ == "__main__":

    print "deleting rendered service path"
    delete(controller, DEFAULT_PORT, get_rendered_service_path_uri())
    time.sleep(1)
