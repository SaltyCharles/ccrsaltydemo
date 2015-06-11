'''
AWS Route 53 Management

:maintainer:    Robert Booth <robert.booth@trebortech.com>
:maturity:      new
:depends:       boto library
:platform:      AWS


'''

# Import salt libs
import salt.utils
import re

# Import supporting libs
try:
    from boto.route53 import Route53Connection as route53
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


def __virtual__():
    if not HAS_BOTO:
        return False
    return True

################################################
# DNS Management
################################################


def get_dns_record(url, aws_access, aws_secret, zonename=None):
    '''
    Get the DNS record

    '''
    r53conn = route53(aws_access, aws_secret)
    if zonename == None:
        zonename = re.sub('^\w*\.', '', url) + '.'
    zone = r53conn.get_zone(zonename)
    if zone:
        dnsobj = zone.get_a(url)
    else:
        return


def create_dns_record(recordtype, url, ip, ttl, aws_access, aws_secret, zonename=None):
    '''
    Create a new a record
    '''
    r53conn = route53(aws_access, aws_secret)
    if zonename == None:
        zonename = re.sub('^\w*\.', '', url) + '.'
    zone = r53conn.get_zone(zonename)
    if zone:
        dnsobj = zone.add_record(recordtype, url, ip, ttl)
    else:
        return
