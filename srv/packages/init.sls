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