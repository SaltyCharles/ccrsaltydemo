# File: /srv/salt/httpd.sls:
{% set pkg_to_install = httpd %}

{{ pkg_to_install }}:
  pkg:
    - installed
  service:
    - running

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['slack']['slack_channel'] }}
     - from_name: {{ pillar['slack']['from_name'] }}
     - message: '{{ pkg_to_install }} was just installed on {{ grains['id'] }}'
     - api_key: {{ pillar['slack']['slack_api'] }}