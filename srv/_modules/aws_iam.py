'''
AWS User Management

:maintainer:    Robert Booth <robert.booth@trebortech.com>
:maturity:      new
:depends:       boto library
:platform:      AWS


'''

# Import salt libs
import salt.utils

# Import supporting libs
try:
    from boto.iam import IAMConnection as iam
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


def __virtual__():
    if not HAS_BOTO:
        return False
    return True


################################################
# User Management
################################################

def getuser(username, aws_access, aws_secret):
    '''
    Retrieve the AWS user information
    '''
    iamconn = iam(aws_access, aws_secret)

    ret = False
    awsUser = iamconn.get_user(username)

    try:
        if len(awsUser) == 1:
            ret = str(awsUser.user.user_id)
        else:
            ret = False
    except NameError:
        ret = False

    return ret


def createuser(username, aws_access, aws_secret):
    # Create new user in AWS

    iamconn = iam(aws_access, aws_secret)

    ret = False
    awsUserID = iamconn.create_user(username)

    try:
        ret = awsUserID
    except NameError:
        ret = False

    return ret

################################################
# Group Management
################################################


def create_group(group_name, aws_access, aws_secret):
    iamconn = iam(aws_access, aws_secret)
    # Check to see if group exist
    objGroup = iamconn.create_group(group_name)

    if objGroup:
        return objGroup
    else:
        return False


def add_user_to_group(group_name, user_name, aws_access, aws_secret, force=False):
    iamconn = iam(aws_access, aws_secret)

    # Check to see if group exist
    iamconn.add_user_to_group(group_name, user_name)
