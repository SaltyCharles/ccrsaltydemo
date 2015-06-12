###############################
#
# All system deployments
#
###############################

  # State files
base:
  'docker*':
    - grains:
      - roles: docker
  'AllSystems': &AllSystems
    - match: compound
    - packages
    - pip
    - users.demo
    - ssh-init
    - grains:
      - company: SaltStack
      - location: San Diego
      - environment: base

  # Servers

  'G@kernel:linux': *AllSystems
  'G@roles:docker':
    - match: compound
    - docker
    - nginx.docker

orchestrate_demo:
  '*':
    - vim
  'orch*':
    - git
    - webserver
  'minion02':
    - mongodb

development:
  'dev*':
    - grains:
      - company: SaltStack
      - location: San Diego
      - environment: development
