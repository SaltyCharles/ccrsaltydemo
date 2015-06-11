# File: /srv/salt/redis.sls

redis:
  pkg:
    - installed
  service:
    - running

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['demose']['slack_channel'] }}
     - from_name: Salty Packager
     - message: 'redis was just installed on {{ grains['id'] }} and the service was started.'
     - api_key: {{ pillar['demose']['slack_api'] }}