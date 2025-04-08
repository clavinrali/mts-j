# This Dockerfile is used to configure and build a Docker image for the client-side 
# application of the "mts-j" project. It utilizes the official Nginx image as the base 
# to serve the static files of the client application.
# Use the official Nginx image
FROM nginx:alpine

# Copier les fichiers du site dans le répertoire par défaut de Nginx
COPY . /usr/share/nginx/html

# Exposer le port 80
EXPOSE 80

# Lancer Nginx
CMD ["nginx", "-g", "daemon off;"]