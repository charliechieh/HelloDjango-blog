FROM nginx:1.17.1

# 替换为国内源（服务器在境外可不替换）
# RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
# COPY ./compose/production/nginx/sources.list /etc/apt/
RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/HelloDjango-blog.conf /etc/nginx/conf.d/HelloDjango-blog.conf