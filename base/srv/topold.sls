# File: /srv/salt/top.sls

base:
  '*':
    - vim
  '*beacon':
    - cherrypy
  '*web':
    - httpd
    - python
    - python.django
  '*redis':
    - redis
  '*archive':
    - archive
  'nginx*':
    - nginx
  'riak*':
    - riak
  'demo-magnolia*':
    - jre
    - magnolia
    - mysql.python-mysqldb
  'salt-master':
    - mysql
    - mysql.python-mysqldb
  'wordpress*':
    - wordpress
  'salt*':
    - mysql.python-mysqldb

