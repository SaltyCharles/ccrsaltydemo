# File: /srv/salt/python/init.sls

python-pkgs:
  pkg:
    - installed
    - names:
      - python
      - pypy
      - python-mako
