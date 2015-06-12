###############################
#
# Manage the /etc/hosts file on minion
#
###############################

{% set hosts = pillar.get('hosts', {}) %}

{% for host in hosts %}
{{ host.name }}:
  host.present:
    - ip:
      - {{ host.ip }}
    - names:
      - {{ host.name }}
{% endfor %}