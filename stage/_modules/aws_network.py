'''
AWS Network Management

:maintainer:    Robert Booth <robert.booth@trebortech.com>
:maturity:      new
:depends:       boto library
:platform:      AWS


'''

# Import salt libs
import salt.utils
import time

# Import supporting libs
try:
    from boto.vpc import VPCConnection as vpc
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


def __virtual__():
    if not HAS_BOTO:
        return False
    return True


################################################
# Network (VPC) Management
################################################

def get_network(network, aws_access, aws_secret):
    '''
    Get the NETWORK(VPC) id

    '''
    vpcconn = vpc(aws_access, aws_secret)

    ret = False

    filters = {'cidr_block': network}
    awsNetwork = vpcconn.get_all_vpcs(filters=filters)

    try:
        if len(awsNetwork) == 1:
            ret = awsNetwork
        else:
            ret = False
    except NameError:
        ret = False
    return ret

################################################
# Subnet Management
################################################


def get_subnet(subnet, aws_access, aws_secret):
    '''
    Get subnet from AWS
    '''
    vpcconn = vpc(aws_access, aws_secret)

    ret = False
    filters = {'cidr_block': subnet}
    objSubnet = vpcconn.get_all_subnets(filters=filters)

    try:
        if len(objSubnet) == 1:
            ret = objSubnet  # str(awsSubnet[0].tags['Name'])
        else:
            ret = False
    except NameError:
        ret = False
    return ret


def create_subnet(network, subnet, subnetname, zone, aws_access, aws_secret):
    # Create network in AWS

    vpcconn = vpc(aws_access, aws_secret)

    objVPC = get_network(network, aws_access, aws_secret)[0]

    if objVPC == False:
        return False
    else:
        objSubnet = vpcconn.create_subnet(
            vpc_id=objVPC.id, cidr_block=subnet, availability_zone=zone)
        if objSubnet:
            # Tag the subnet
            newTags = {
                'Name': subnetname,
                'Createdby': 'salt'
            }

            tag_object(vpcconn, objSubnet.id, newTags)
            return get_subnet(subnet, aws_access, aws_secret)
        else:
            return False

################################################
# ACL Management
################################################


def get_network_acl(aclname, aws_access, aws_secret):
    # Check to see if network acl already exist by name
    # Return object if exist else False

    vpcconn = vpc(aws_access, aws_secret)

    ret = False
    filters = {'tag:Name': aclname}
    objNetACL = vpcconn.get_all_network_acls(filters=filters)

    try:
        if len(objNetACL) == 1:
            ret = objNetACL
        else:
            ret = False
    except NameError:
        ret = False
    return ret


def create_network_acl(network, subnetid, aclname, aws_access, aws_secret):
    # Create network ACL in AWS
    vpcconn = vpc(aws_access, aws_secret)
    objVPC = get_network(network, aws_access, aws_secret)[0]

    if objVPC == False:
        return False
    else:
        objNetACL = vpcconn.create_network_acl(vpc_id=objVPC.id)
        if objNetACL:
            # Tag the network ACL
            newTags = {
                'Name': aclname,
                'Createdby': 'salt'
            }
            tag_object(vpcconn, objNetACL.id, newTags)
            vpcconn.associate_network_acl(objNetACL.id, subnetid)
            return get_network_acl(aclname, aws_access, aws_secret)
        else:
            return False

################################################
# ACL Entry Management
################################################


def clean_network_acl_entry(aclname, aws_access, aws_secret):
    vpcconn = vpc(aws_access, aws_secret)
    networkacl = get_network_acl(aclname, aws_access, aws_secret)[0]

    for rule in networkacl.network_acl_entries:
        if rule.rule_number < 32767:  # 32767 is the default rule
            vpcconn.delete_network_acl_entry(
                networkacl.id, rule.rule_number, rule.egress)
    return True


def create_network_acl_entry(aclid,
                             rule_number,
                             protocol,
                             rule_action,
                             cidr_block,
                             egress,
                             port_range_from,
                             port_range_to,
                             aws_access,
                             aws_secret):
    vpcconn = vpc(aws_access, aws_secret)

    vpcconn.create_network_acl_entry(
        network_acl_id=aclid,
        rule_number=rule_number,
        protocol=protocol,
        rule_action=rule_action,
        cidr_block=cidr_block,
        egress=egress,
        port_range_from=port_range_from,
        port_range_to=port_range_to)
    return True

################################################
# Route Table Management
################################################


def get_route_table(routetablename, aws_access, aws_secret):
    vpcconn = vpc(aws_access, aws_secret)

    ret = False
    filters = {'tag:Name': routetablename}
    objRouteTable = vpcconn.get_all_route_tables(filters=filters)

    try:
        if len(objRouteTable) == 1:
            ret = objRouteTable
        else:
            ret = False
    except NameError:
        ret = False
    return ret


def create_route_table(network, routetablename, subnetid, aws_access, aws_secret):
    vpcconn = vpc(aws_access, aws_secret)
    objVPC = get_network(network, aws_access, aws_secret)[0]

    if objVPC == False:
        return False
    else:
        objRouteTable = vpcconn.create_route_table(vpc_id=objVPC.id)
        if objRouteTable:
            # Tag the network ACL
            newTags = {
                'Name': routetablename,
                'Createdby': 'salt'
            }
            tag_object(vpcconn, objRouteTable.id, newTags)
            vpcconn.associate_route_table(objRouteTable.id, subnetid)
            return get_route_table(routetablename, aws_access, aws_secret)
        else:
            return False

################################################
# Route Table Entry Management
################################################


def create_route_table_entry(routetableid, cidr, dsttype, dstitem, aws_access, aws_secret):
    vpcconn = vpc(aws_access, aws_secret)

    if dsttype == 'interface':
        vpcconn.create_route(
            route_table_id=routetableid,
            destination_cidr_block=cidr,
            interface_id=dstitem)
    elif dsttype == 'instance':
        vpcconn.create_route(
            route_table_id=routetableid,
            destination_cidr_block=cidr,
            instance_id=dstitem)
    elif dsttype == 'gateway':
        vpcconn.create_route(
            route_table_id=routetableid,
            destination_cidr_block=cidr,
            gateway_id=dstitem)
    return True

################################################
# Module Support
################################################


def tag_object(vpcconn, objectid, newTags):
    time.sleep(3)
    vpcconn.create_tags(objectid, newTags)
    return True
