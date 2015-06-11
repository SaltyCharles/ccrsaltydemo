# File: /srv/salt/archive.sls

install_archive_pkgs:
  pkg.installed:
    - names:
      - rsync
      - sharutils
      - vsftpd

  service.running:
    - name: vsftpd
    - enable: True

# File: /srv/salt/notifications.sls

"Notification of install":
  slack.post_message:
    - channel: {{ pillar['demose']['slack_channel'] }}
    - from_name: 'SaltyCharles-API'
    - message: 'rsync, sharutils, vsftpd have been installed on {{ grains['id'] }}'
    - api_key: {{ pillar['demose']['api_key'] }}
