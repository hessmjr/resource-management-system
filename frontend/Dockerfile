FROM nginx:alpine

# Copy static files
COPY frontend/static /usr/share/nginx/html/static
COPY frontend/templates /usr/share/nginx/html/templates

# Copy nginx configuration
COPY frontend/nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]