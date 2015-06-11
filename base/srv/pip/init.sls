###############################
#
# Install pip modules from pip pillar
#
###############################

# Make sure PIP is updated
"Update PIP":
  cmd.run:
    - name: 'easy_install -U pip'
    - require:
      - pkg: 'Python Pip'

# Install pip packages

{% set packages = pillar.get('pip', {}) %}

{% for package in packages %}
{{ package.name }}:
  pip.installed:
    - name: {{ package.packagename }}
    {% if package.required is defined %}
    - require:
      - pkg: {{ package.required }}
    {% endif %}
{% endfor %}

# File: /srv/salt/notifications.sls

"Notification of install":
  slack.post_message:
    - channel: {{ pillar['demose']['api_channel'] }}
    - from_name: 'SaltyCharles-API'
    - message: '{{ package.name }} has been installed on {{ grains['id'] }}'
    - api_key: {{ pillar['demose']['api_key'] }}