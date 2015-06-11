nginx:
  pkg:
    - installed
    - require_in:

  service:
    - running
    - require:
      - pkg: nginx
