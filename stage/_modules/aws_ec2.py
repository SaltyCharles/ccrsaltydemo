'''
AWS Network Management

:maintainer:    Robert Booth <robert.booth@trebortech.com>
:maturity:      new
:depends:       boto library
:platform:      AWS


'''
# Import salt libs
import salt.utils

# Import supporting libs
try:
    from boto.ec2 import EC2Connection as ec2
    from boto.ec2 import networkinterface as botointerface
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


def __virtual__():
    if not HAS_BOTO:
        return False
    return True


import time

################################################
# Public IP Management
################################################

def get_public_ip(aws_access, aws_secret):
    '''
    Get public IP

    '''
    ec2conn = ec2(aws_access, aws_secret)
    objIP = ec2conn.allocate_address('vpc')
    return objIP

def associate_public_ip(networkintid, pubipid, aws_access, aws_secret):
    ec2conn = ec2(aws_access, aws_secret)
    return ec2conn.associate_address(
        network_interface_id=networkintid,
        allocation_id=pubipid)

def create_interface(subnetid, privip, description, secgroup, aws_access, aws_secret):
    ec2conn = ec2(aws_access, aws_secret)

    objInterface = ec2conn.create_network_interface(
        subnet_id=subnetid,
        private_ip_address=privip,
        description=description,
        groups=secgroup)

    if objInterface:
        # Tag the interface
        newTags = {
            'Name': description,
            'Createdby': 'salt'
        }
        tag_object(ec2conn, objInterface.id, newTags)

    return objInterface


################################################
# Security Group Management
################################################


def get_security_group(sggroupname, aws_access, aws_secret):
    ec2conn = ec2(aws_access, aws_secret)

    objSecurityGroup = ec2conn.get_all_security_groups(
        groupnames=sggroupname)[0]

    return objSecurityGroup


def create_security_group(sgname, sgdescription, vpcid, aws_access, aws_secret):

    ec2conn = ec2(aws_access, aws_secret)

    objSecurityGroup = ec2conn.create_security_group(
        name=sgname,
        description=sgdescription,
        vpc_id=vpcid)

    if objSecurityGroup:
        # Tag the Security Group
        newTags = {
            'Createdby': 'salt'
        }
        tag_object(ec2conn, objSecurityGroup.id, newTags)

    return objSecurityGroup

################################################
# Security Group Entry Management
################################################


def get_security_group_entry(aws_access, aws_secret):

    return


def create_security_group_entry(sggroupid, protocol, fromport, toport, cidr, egress, aws_access, aws_secret):
    ec2conn = ec2(aws_access, aws_secret)

    if egress:
        # This section is for egress
        ec2conn.authorize_security_group_egress(
            group_id=sggroupid,
            ip_protocol=protocol,
            from_port=fromport,
            to_port=toport,
            cidr_ip=cidr)
    else:
        # This section is for ingress
        ec2conn.authorize_security_group_ingress(
            group_id=sggroupid,
            ip_protocol=protocol,
            from_port=fromport,
            to_port=toport,
            cidr_ip=cidr)

    return


################################################
# Security Groups
################################################


def get_securitygroup_ids(securitygroups, aws_access, aws_secret):
    ec2conn = ec2(aws_access, aws_secret)
    groupid = []

    try:
        collsecuritygroups = ec2conn.get_all_security_groups()

        for group in collsecuritygroups:
            if group.name in securitygroups:
                groupid.append(group.id)

    except AttributeError:
        return False

    return groupid

################################################
# Instance Management
################################################

def get_instance_by_intid(intid, aws_access, aws_secret):
    ec2conn = ec2(aws_access, aws_secret)

    # Check to see if interface is connected to an instance and return that
    # instance

    try:
        instanceid = ec2conn.get_all_network_interfaces(
            network_interface_ids=[intid])[0].attachment.instance_id

        if instanceid:
            instanceobj = ec2conn.get_only_instances(instance_ids=[instanceid])
            return instanceobj
        else:
            return False
    except AttributeError:
        return False


def create_instance(amiid,
                    keyname,
                    customertag,
                    userdata,
                    instancetype,
                    intid,
                    protect,
                    instancename,
                    aws_access,
                    aws_secret):
    
    ec2conn = ec2(aws_access, aws_secret)
    
    interface = botointerface.NetworkInterfaceSpecification(network_interface_id=intid)
    interfacecoll = botointerface.NetworkInterfaceCollection(interface)

    newinstance = ec2conn.run_instances(
        image_id=amiid,
        key_name=keyname,
        user_data=userdata,
        instance_type=instancetype,
        network_interfaces=interfacecoll,
        disable_api_termination=protect)

    if newinstance:
        # Tag the Instance
        newTags = {
            'Name': instancename,
            'Customer': customertag,
            'Createdby': 'salt'
        }
        # Check if instance exist
        instanceid = newinstance.instances[0].id
        for x in range(0,4):
            instanceobj = ec2conn.get_all_instances(instance_ids=[instanceid])
            if instanceobj:
                tag_object(ec2conn, instanceid, newTags)
                break

    return newinstance


################################################
# Network Interface Management
################################################

def get_interface(interfacename, aws_access, aws_secret):
    '''
    Get interface information
    '''

    ec2conn = ec2(aws_access, aws_secret)

    ret = False
    filters = {'tag:Name': interfacename}
    objNetworkInterface = ec2conn.get_all_network_interfaces(filters=filters)

    try:
        if len(objNetworkInterface) == 1:
            ret = objNetworkInterface
        else:
            ret = False
    except NameError:
        ret = False
    return ret

################################################
# Module support
################################################


def tag_object(ec2conn, objectid, newTags):
    time.sleep(3)

    ec2conn.create_tags(objectid, newTags)
    return True
