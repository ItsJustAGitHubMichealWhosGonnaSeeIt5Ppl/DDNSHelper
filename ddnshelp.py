## IMPORTS ##
# BUILT-IN 
from os import getenv
import sys
import argparse
import logging
from datetime import datetime

# EXTERNAL
from porkbun_api import Porkbun
#TODO better security for storing key
from dotenv import load_dotenv

# INTERNAL

## CODE ##
# Log setup stuff
logging.basicConfig(filename='ddnshelper.log', 
level=logging.WARNING, 
format='%(asctime)s | %(name)s | %(funcName)s | %(levelname)s | %(message)s', 
datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("DDNSHelper")

load_dotenv()
supported_registrars = ["porkbun"]

# Moved to its own function so I can set up tests
def update_ddns(registrar:str, domain:str):
    
    if registrar.lower() not in supported_registrars:
        raise ValueError(f"Registrar '{registrar}' is not currently supported.")
    
    logger.debug(f"Registrar: {registrar}\nDomain: {domain}")
    
    if registrar.lower() == "porkbun": # Porkbun setup
        API_KEY = getenv("PORKBUN_KEY", None)
        API_SECRET = getenv("PORKBUN_SECRET", None)
        if API_KEY == None or API_SECRET == None:
            raise Exception("Missing API key or secret")
        
        else:
            logger.info("Successfully loaded enviroment variables")
            # Not sure if this is safe, but who cares
            logger.debug(f"API Key starts with: {API_KEY[:5]}")
            logger.debug(f"API Secret starts with: {API_SECRET[:5]}")
        
        pb = Porkbun(API_KEY, API_SECRET)
        
        # THE ACTUAL SCRIPT PART
        logger.info("Getting current IP")
        ip = pb.ping().yourIp
        #TODO support subdomains with multiple "." Currently the domain worker.team.mydomain.com would not work
        domain_split = domain.split(".") # Split up the domain 
        
        domain = ".".join(domain_split[1:])
        subdomain = domain_split[0]
        logger.debug(f"Getting current DNS record for domain: {domain}, subdomain: {subdomain}")
        record = pb.dns.get_record(domain=domain, subdomain=subdomain, record_type="A")[0]
        print("Getting IP")
        logger.debug(f"Current IP: {ip}, Current DNS record: {record['content']}")
        if record['content'] == ip: # IP is already up to date, no changes are needed :)
            logger.info("IP already up to date")
            
        else: # Not the same, update!
            note = f"Automatically updated by DDNSHelper on {datetime.now()}"
            resp = pb.dns.update_record(domain=".".join(domain_split[1:]), record_id=record['id'], content=ip, name=domain_split[0], record_type=record['type'], ttl=record['ttl'], priority=record['prio'], notes=note)
            if resp.get("status") == "Success":
                logger.info("IP updated successfully")
            else:
                logging.error(f"Failed to update IP. API returned {resp}")

#TODO allow logging settings to be set with args (logfile name, no logfile, loglevel)
#TODO allow more of the DNS settings to be set with args (TTL, note, better subdomain handling)
parser = argparse.ArgumentParser(
    prog="DDNSHelper",
    description="Simple tool to update DNS records for supported registrars"
)

# Required args
parser.add_argument("registrar", type=str, help=f"The registrar. Supported registrars are: {','.join(supported_registrars)}")
parser.add_argument("domain", type=str, help="The full domain to be updated")

# Optional args
parser.add_argument("--log_level", help="Set logging level. Supported levels are 'debug', 'info', 'warning', 'error', 'critical'. Defaults to 'warning'")

args = parser.parse_args()
print(args)

registrar = args.registrar
domain = args.domain

# Parse optional arguments
if args.log_level and args.log_level.lower() in ['debug', 'info', 'warning', 'error', 'critical']:
    #TODO there is probably a nicer way to do this lol
    match args.log_level.lower():
        case 'debug':
            logger.setLevel(level=logging.DEBUG)
        case 'info':
            logger.setLevel(level=logging.INFO)
        case 'warning':
            logger.setLevel(level=logging.WARNING)
        case 'error':
            logger.setLevel(level=logging.ERROR)
        case 'critical':
            logger.setLevel(level=logging.CRITICAL)

print("Running now")
update_ddns(registrar=registrar, domain=domain)