####################################
#
# Install 7zip MSI
#
####################################
{% set pkg_to_install = 7zip %}

# Stop service
"Stop the W3SVC":
  win_service.stop:
    - name: W3SVC


# Install
"Install 7Zip":
  pkg.installed:
    - name: {{ pkg_to_install }}
    - version: 9.20.00.0
    #- version: 9.38.00.0
    - require:
      - win_service: "Stop the W3SVC"


# Restart service
"Start the W3SVC":
  win_service.start:
    - name: W3SVC

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['slack']['slack_channel'] }}
     - from_name: {{ pillar['slack']['from_name'] }}
     - message: '{{ pkg_to_install }} was just installed on {{ grains['id'] }} and the template was updated.'
     - api_key: {{ pillar['slack']['slack_api'] }}