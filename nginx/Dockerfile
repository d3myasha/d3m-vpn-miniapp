FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

# Создаём директорию для SSL сертификатов
RUN mkdir -p /etc/nginx/ssl

# Создаём директорию для Let's Encrypt
RUN mkdir -p /var/www/certbot

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
