'''
Manage deployment of IIS websites via WebAdministration powershell module

:maintainer:    Robert Booth <rbooth@saltstack.com>
:maturity:      new
:depends:       Windows
:platform:      Windows

'''


# Import salt libs
import salt.utils
# Define the module's virtual name
__virtualname__ = 'win_iis'

def __virtual__():
    '''
    Load only on Windows
    '''
    if salt.utils.is_windows():
        return __virtualname__
    return False

def _srvmgr(func):
    '''
    Execute a function from the WebAdministration PS module
    '''

    return __salt__['cmd.run'](
        'Import-Module WebAdministration; {0}'.format(func),
        shell='powershell',
        python_shell=True)

def list_sites():
    '''
    List all the currently deployed websites
    
    CLI Example:

    .. code-block:: bash

        salt '*' win_iis.list_sites
    '''
    pscmd = []
    pscmd.append("Get-WebSite -erroraction silentlycontinue -warningaction silentlycontinue")
    pscmd.append(" | foreach {")
    pscmd.append(" $_.Name")
    pscmd.append("};")

    
    command = ''.join(pscmd)
    return _srvmgr(command)

def create_site(name, protocol, sourcepath, port, apppool='', hostheader='', ipaddress=''):
    '''
    Create a basic website in IIS

    CLI Example:

    .. code-block:: bash

        salt '*' win_iis.create_site name='My Test Site' protocol='http' sourcepath='c:\stage' port='80' apppool='TestPool'

    '''

    pscmd = []
    pscmd.append("cd IIS:\Sites\;")
    pscmd.append("New-Item 'iis:\Sites\{0}'".format(name))
    pscmd.append(" -bindings @{{protocol='{0}';bindingInformation=':{1}:{2}'}}".format(protocol, port, hostheader.replace(" ","")))
    pscmd.append("-physicalPath {0};".format(sourcepath))

    if apppool:
        pscmd.append("Set-ItemProperty 'iis:\Sites\{0}'".format(name))
        pscmd.append(" -name applicationPool -value '{0}';".format(apppool))

    command = ''.join(pscmd)
    return _srvmgr(command)

def remove_site(name):
    '''
    Delete website from IIS

    CLI Example:

    .. code-block:: bash

        salt '*' win_iis.remove_site name='My Test Site'

    '''

    pscmd = []
    pscmd.append("cd IIS:\Sites\;")
    pscmd.append("Remove-WebSite -Name '{0}'".format(name))

    command = ''.join(pscmd)
    return _srvmgr(command)


def list_apppools():
    '''
    List all configured IIS Application pools
    
    CLI Example:

    .. code-block:: bash

        salt '*' win_iis.list_apppools
    '''
    pscmd = []
    pscmd.append("Get-ChildItem IIS:\AppPools\ -erroraction silentlycontinue -warningaction silentlycontinue")
    pscmd.append(" | foreach {")
    pscmd.append(" $_.Name")
    pscmd.append("};")

    
    command = ''.join(pscmd)
    return _srvmgr(command)


def create_apppool(name):
    '''
    Create IIS Application pools
    
    CLI Example:

    .. code-block:: bash

        salt '*' win_iis.create_apppool name='MyTestPool'
    '''
    pscmd = []
    pscmd.append("New-Item 'IIS:\AppPools\{0}'".format(name))
        
    command = ''.join(pscmd)
    return _srvmgr(command)

def remove_apppool(name):
    '''
    Removes IIS Application pools
    
    CLI Example:

    .. code-block:: bash

        salt '*' win_iis.remove_apppool name='MyTestPool'
    '''
    pscmd = []
    pscmd.append("Remove-Item 'IIS:\AppPools\{0}' -recurse".format(name))

    command = ''.join(pscmd)
    return _srvmgr(command)


