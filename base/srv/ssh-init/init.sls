"Update ChallengeResponseAuthentication":
  file.replace:
    - name: '/etc/ssh/sshd_config'
    - pattern: 'ChallengeResponseAuthentication yes'
    - repl: 'ChallengeResponseAuthentication no'

"Update PrintMotd":
  file.replace:
    - name: '/etc/ssh/sshd_config'
    - pattern: 'PrintMotd no'
    - repl: 'PrintMotd yes'

"Update UsePAM":
  file.replace:
    - name: '/etc/ssh/sshd_config'
    - pattern: 'UsePAM no'
    - repl: 'UsePAM yes'

"Update PasswordAuthentication":
  file.replace:
    - name: '/etc/ssh/sshd_config'
    - pattern: 'PasswordAuthentication no'
    - repl: 'PasswordAuthentication yes'

RestartSSHD:
  cmd.run:
    - name: 'service ssh restart'
    - cwd: '/'
    - stateful: False
    - watch:
      - file: "Update ChallengeResponseAuthentication"
      - file: "Update PrintMotd"
      - file: "Update UsePAM"
      - file: "Update PasswordAuthentication"