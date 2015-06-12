{% if grains['os_family'] == 'RedHat' %}
{% set vim = 'vim-enhanced' %}
{% else %}
{% set vim = 'vim' %}
{% endif %}
{{ vim }}:
  pkg.installed

emacs:
  pkg.installed

/root/.vimrc:
  file:
    - managed
    - source: salt://vim/vimrc_tmpl
    - require:
      - pkg: vim

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['slack']['slack_channel'] }}
     - from_name: {{ pillar['slack']['from_name'] }}
     - message: '{{vim}} was just installed on {{ grains['id'] }} and the template was updated.'
     - api_key: {{ pillar['slack']['slack_api'] }}