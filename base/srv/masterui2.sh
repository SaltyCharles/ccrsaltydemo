apt-get update
apt-get upgrade -y
wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
apt-get install python-mysqldb -y
userdel ubuntu
useradd -p $(openssl passwd -1 saltme) ubuntu
usermod -a -G sudo ubuntu
mkdir /stage
cd /stage
mkdir /srv/salt
mkdir -p /etc/salt/master.d
curl -L https://bootstrap.saltstack.com -o install_salt.sh
sh install_salt.sh -M -P git 2015.2
cat > /srv/salt/create-ssl-certs.sls <<EOF
include:
  - pyopenssl-install
  
create cert for salt-api:
  module.run:
    - name: tls.create_self_signed_cert
    - tls_dir: salt_api
    - require:
      - sls: pyopenssl-install
EOF

cat > /srv/salt/pyopenssl-install.sls <<EOF
pyopenssl:
  pip.installed:
    - name: PyOpenSSL
    - exists_action: i
    - reload_modules: True
EOF
salt-call --local state.sls create-ssl-certs
pip install cherrypy==3.2.3
wget https://jenkins-production.saltstack.com/e-pkg/srv.tgz
tar -xvf srv.tgz -C /
cat > /etc/salt/master.d/sse.conf <<EOF
external_auth:
    pam:
      ubuntu:
        - '.*'
        - '@runner'
        - '@wheel'
    
rest_cherrypy:
    port: 8000
    debug: False
    disable_ssl: False
    ssl_crt: '/etc/pki/salt_api/certs/localhost.crt'
    ssl_key: '/etc/pki/salt_api/certs/localhost.key'
    
# Please replace mysql.host by your hostname
mysql.host: 'localhost'
mysql.user: 'saltadmin'
# Please replace the password to use your password
mysql.pass: 'saltadmin'
mysql.db: 'saltdb'
mysql.port: 3306
#mysql.ssl_ca: '/etc/pki/mysql/certs/<sse host>.pem'
    
master_job_cache: mysql
    
loop_interval: 60
presence_events: True
    
event_return: mysql
EOF
salt-call --local state.sls sso pillar='{"sso": {"db_password": "saltadmin", "su_user": "saltadmin", "su_pass": "saltadmin"}}'
service salt-master restart
service salt-api restart