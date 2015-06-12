# File: /srv/salt/redis.sls

redis:
  pkg:
    - installed
  service:
    - running

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['slack']['slack_channel'] }}
     - from_name: {{ pillar['slack']['from_name'] }}
     - message: 'redis was just installed on {{ grains['id'] }} and the service was started.'
     - api_key: {{ pillar['slack']['slack_api'] }}