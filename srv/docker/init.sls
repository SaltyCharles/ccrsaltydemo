###############################
#
# Install dev version of docker
#
###############################

Docker-Testing-Branch:
  pkg.installed:
    - name: docker.io
    - refresh: True


base:
  pkgrepo.managed:
    - name: ppa:docker-maint/testing
    - file: /etc/apt/sources.list.d/docker-maint.list
    - keyid: 3BD7709A
    - keyserver: keyserver.ubuntu.com
    - require_in:
      - pkg: Docker-Testing-Branch

# File: /srv/salt/notifications.sls

"Notification of docker install":
  slack.post_message:
    - channel: {{ pillar['slack']['slack_channel'] }}
    - from_name: {{ pillar['slack']['from_name'] }}
    - message: 'Docker Testing Branch has been installed on {{ grains['id'] }}'
    - api_key: {{ pillar['slack']['slack_api'] }}