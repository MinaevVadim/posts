FROM nginx

COPY nginx_configuration.conf etc/nginx/nginx.conf
COPY nginx_default.conf etc/nginx/conf.d/default.conf
