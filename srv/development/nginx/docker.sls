###############################
#
# Deploy nginx on docker
#
###############################

# Download image from repository if it doesn't already exists
download-corp-image:
  docker.pulled:
    - name: saltme/nginx
    - tag: 0.6



# Deploy the containers if they don't already exists
{% set nginxRunning = 2 %}
{% set nginxStopUpto = 2 %}

{% for nginx_server in range(nginxRunning) %}

run-nginx{{ nginx_server }}-container:
  docker.running:
    - name: Nginx{{ nginx_server }}
    - image: saltme/nginx:0.6
    - ports:
        "80/tcp":
            HostIp: "0.0.0.0"
            HostPort: "800{{ nginx_server }}"
    - publish_all_ports: True
    - volumes:
      - /demo/web/site1:
          bind: /usr/share/nginx/html
          ro: true
    - tty: True
    - stdin_open: True
    - watch:
      - docker: download-corp-image
{% endfor %}


# Clean up of docker containers
{% for remove_nginx_server in range(nginxRunning, nginxStopUpto) %}
run-nginx{{ remove_nginx_server }}-container:
  docker.absent:
    - name: Nginx{{ remove_nginx_server }}
{% endfor %}