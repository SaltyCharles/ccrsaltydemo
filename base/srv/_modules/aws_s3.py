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
    from boto.s3.connection import S3Connection as s3
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False


def __virtual__():
    if not HAS_BOTO:
        return False
    return True


################################################
# S3 Object Management
################################################

def get_object_as_string(objectid, bucketname, aws_access, aws_secret):
    '''
    Get object from S3

    '''
    s3conn = s3(aws_access, aws_secret)
    bucket = s3conn.get_bucket(bucketname)
    objectkey = bucket.get_key(objectid)
    if objectkey:
        return objectkey.get_contents_as_string()
    else:
        return


def save_object_as_string(objectid, bucketname, content, aws_access, aws_secret):
    s3conn = s3(aws_access, aws_secret)
    bucket = s3conn.get_bucket(bucketname)
    objectkey = bucket.new_key(objectid)
    objectkey.set_contents_from_string(content)
    return objectkey.get_contents_as_string()


def get_folder():
    return


def create_folder():
    return
