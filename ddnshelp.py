## IMPORTS ##
# BUILT-IN 
from typing import Optional
from os import getenv
from json import loads as jloads
import sys
#TODO logging of some kind

# EXTERNAL
import requests

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
    URL_BASE = "https://api.porkbun.com/api/json/v3/"
    
    global auth_json # Makes it usable in all commands
    auth_json = {
	"secretapikey": API_SECRET,
	"apikey": API_KEY
    }
    
    ## PORKBUN FUNCTIONS # TODO maybe move these to their own home?
    def porkbun_get_ip(): # Use test to get IP
        resp = requests.get(url=URL_BASE+"ping",json=auth_json)
        if resp.status_code != 200:
            raise Exception(resp) # TODO flesh this out and log the error somewhere
        else:
            return jloads(resp.text)["yourIp"]
        
    def porkbun_get_record(domain:str, subdomain:Optional[str]=None, record_type:Optional[str]=None, record_id:Optional[int|str]=None):
        if record_id == None and (subdomain == None or record_type == None):
            raise ValueError("Must provide a DNS record ID or subdomain and record type")
        
        url = f"/dns/retrieveByNameType/{domain}/"
        if record_id != None:
            url += record_id
        else:
            url += f"{record_type}/{subdomain}"

        resp = requests.post(url=URL_BASE+url,json=auth_json)
        if resp.status_code != 200:
            raise Exception(resp) # TODO flesh this out and log the error somewhere
        elif len(jloads(resp.text)['records']) == 0:
            raise Exception(resp) #TODO bad
        else:
            return jloads(resp.text)['records'][0] # Select the record
    
    def porkbun_update_record(domain:str, content:str, record_id:Optional[int|str], name:Optional[str]=None, record_type:Optional[str]=None, ttl:Optional[int]=None, priority:Optional[int]=None, notes:Optional[int]=None): # Record is optional in case I decide to add edting by subdomain and type later
        # if name is not provided it'll wipe it out 
        if name == None or ttl == None or priority == None or notes == None or record_type == None: # Get the current record information to fill in
            record = porkbun_get_record(domain=domain, record_id=record_id)
        
        query = f"dns/edit/{domain}/{record_id}"
        
        changes = {
            **auth_json, # Add the auth stuff to the json we're gonna send
            "name": name if name != None else record['name'],
            "type": record_type if record_type != None else record['type'],
            "content": content,
            "ttl": ttl if ttl != None else record['ttl'],
            "prio": priority if priority != None else record['prio'],
            "notes": notes if notes != None else record['notes']
            }
        
        resp = requests.post(url=URL_BASE+query,json=changes)
        if resp.status_code != 200 or jloads(resp.text)['status'] != "SUCCESS":
            raise Exception(resp) # TODO flesh this out and log the error somewhere
    
    
    # THE ACTUAL SCRIPT PART
    ip = porkbun_get_ip() # This is now the IP
    domain_split = domain.split(".") # Split up the domain #TODO support subdomains with "."
    record = porkbun_get_record(domain=".".join(domain_split[1:]), subdomain=domain_split[0], record_type="A")
    
    if record['content'] == ip: # IP is already up to date, no changes are needed :)
        print("No update needed")
    else: # Not the same, update!
        porkbun_update_record(domain=".".join(domain_split[1:]), record_id=record['id'], content=ip, name=domain_split[0], record_type=record['type'], ttl=record['ttl'], priority=record['prio'], notes=record['notes'])
        print("Updated")