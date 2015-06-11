webserver_stuff:
  pkg:
    - installed
    - pkgs:
      - httpd

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['demose']['slack_channel'] }}
     - from_name: Salty Packager
     - message: 'httpd was just installed on {{ grains['id'] }}'
     - api_key: {{ pillar['demose']['slack_api'] }}