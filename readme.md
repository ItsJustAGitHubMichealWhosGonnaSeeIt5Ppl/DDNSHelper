# Dynanic DNS Helper

W.I.P!!

This is a simple tool to update your DNS records for registrars that don't support a DDNS client.

## Registrar support

### Supported

Registrars that this script currently supports

- [Porkbun](https://porkbun.com/)

### Planned

#### Unsupported

Registrars that I cannot support (but have tried)

- namecheap (Requires whitelisted IP to authorize requests)

## Setup and usage

1. Download `ddnshelp.py` and `constraints.txt`
2. (optional) Set up a virtual environment
3. Install requirements with `pip install -r constraints.txt`
4. Set up your API credentials in a `.env` file
5. Run `ddnshelper.py <Registratr> <Domain>` (can be used with cronjob)

### Registar specific set up

#### Porkbun

You need an API key for Porkbun. See instructions below

1. Create API credentials here: https://porkbun.com/account/api
2. Enable API access for domain(s)
    - A: Enable for all domains (not recommended)
    - B: Selectively enable API access for desired domains (recommended)
3. Update `PORKBUN_KEY` and `PORKBUN_SECRET` variables in the `.env` file

## FAQ

(No one has asked me anything so I'm just guessing what might be asked)

Q: Will you add support for _ registar?  
A: If they are not on the list of unsupported registrars, I'd be happy to try! Submit a feature request with the registrar name.
