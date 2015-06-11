###############################
#
# Install the boto python module via PIP
#
###############################

"Python PIP package install":
  pkg.installed:
    - name: python-pip

"PIP install boto":
  pip.installed:
    - name: boto
    - require:
      - pkg: python-pip