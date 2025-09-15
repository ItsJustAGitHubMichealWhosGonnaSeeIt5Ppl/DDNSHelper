### Dynanic DNS Helper
W.I.P!!

This is a simple tool to update your DNS records for registrars that don't support a DDNS client.


### Registrar support

### Supported
Registrars that this script currently supports
- [Porkbun](https://porkbun.com/)

### Planned

#### Unsupported

Registrars that I cannot support (but have tried)
- namecheap (Requires whitelisted IP to authorize requests)

### Setup and usage
1. Download `ddnshelp.py` and `constraints.txt`
2. Install requirements with `pip install -r constraints.txt`
3. Set up your API credentials in a `.env file`
4. Run `ddnshelp.py <Registratr> <Domain>` (can be used with cronjob)

### FAQ
(No one has asked me anything so I'm just guessing what might be asked)

Q: Will you add support for _ registar?  
A: If they are not on the list of unsupported registrars, I'd be happy to try! Submit a feature request with the registrar name.


## Registrar setup
Registrar specific setup steps
### Porkbun
1. Create API credentials here: https://porkbun.com/account/api
2. Enable API access for domain(s)
    - A: Enable for all domains (not recommended)
    - B: Selectively enable API access for desired domains (recommended)