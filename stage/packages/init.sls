###############################
#
# Install packages from packages pillar
#
###############################

{% set packages = pillar.get('packages', {}) %}

{% for package in packages %}
{{ package.name }}:
  pkg.installed:
    - name: {{ package.packagename }}
    {% if package.required is defined %}
    - require:
      - pkg: package.required
    {% endif %}
{% endfor %}

"Notification of install":
   slack.post_message:
     - channel: {{ pillar['slack']['slack_channel'] }}
     - from_name: {{ pillar['slack']['from_name'] }}
     - message: '{{ package.name }} was just installed on {{ grains['id'] }}'
     - api_key: {{ pillar['slack']['slack_api'] }}