webserver_stuff:
  pkg:
    - installed
    - pkgs:
      - httpd

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['slack']['slack_channel'] }}
     - from_name: {{ pillar['slack']['from_name'] }}
     - message: 'httpd was just installed on {{ grains['id'] }}'
     - api_key: {{ pillar['slack']['slack_api'] }}