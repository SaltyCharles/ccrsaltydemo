# File: /srv/salt/httpd.sls:
{% set pkg_to_install = httpd %}

{{ pkg_to_install }}:
  pkg:
    - installed
  service:
    - running

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['demose']['slack_channel'] }}
     - from_name: Salty Packager
     - message: '{{ pkg_to_install }} was just installed on {{ grains['id'] }}'
     - api_key: {{ pillar['demose']['slack_api'] }}