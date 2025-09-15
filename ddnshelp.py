## IMPORTS ##
# BUILT-IN 
from typing import Optional
from os import getenv
from json import loads as jloads
import sys
#TODO logging of some kind

# EXTERNAL
import requests
from porkbun_api import Porkbun

# INTERNAL

## CODE ##
debug = False # Use to disable args and instead input manual data

if debug:
    registrar = "porkbun"
    domain = "fakedomain.com"
else: # Normal run mode
    if len(sys.argv) != 3:
        raise ValueError(f"Incorrect amount of arguments supplied. Expecting 2, got {str(len(sys.argv)-1)}")

    registrar = sys.argv[1] # registrar
    domain = sys.argv[2] # full domain
    
supported_registrars = ["porkbun"]
if registrar.lower() not in supported_registrars:
    raise ValueError(f"Registrar '{registrar}' is not currently supported.")

if registrar.lower() == "porkbun": # Porkbun setup
    API_KEY = getenv("PORKBUN_KEY")
    API_SECRET = getenv("PORKBUN_SECRET")
    pb = Porkbun(API_KEY, API_SECRET)
    
    
    # THE ACTUAL SCRIPT PART
    ip = pb.ping().yourIp
    domain_split = domain.split(".") # Split up the domain #TODO support subdomains with "."
    
    record = pb.dns.get_record(domain=".".join(domain_split[1:]), subdomain=domain_split[0], record_type="A")[0]
    
    if record['content'] == ip: # IP is already up to date, no changes are needed :)
        print("No update needed")
    else: # Not the same, update!
        pb.dns.update_record(domain=".".join(domain_split[1:]), record_id=record['id'], content=ip, name=domain_split[0], record_type=record['type'], ttl=record['ttl'], priority=record['prio'], notes=record['notes'])
        print("Updated")