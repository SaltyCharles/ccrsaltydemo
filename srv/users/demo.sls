demo:
  user.present:
    - fullname: demo
    - shell: '/bin/bash'
    - password: '$1$xyz$K1m3vkKZXL1p36LriRJHK0'
    - optional_groups:
      - wheel
      - admin
      - sudo
