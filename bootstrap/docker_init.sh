#!/bin/bash

# < !--- install some useful network tools for the VM --!>
sudo apt install net-tools

# <!------ domain / SSL  configuration -------!>

# Set up the domain name 
DOMAIN_NAME="checkmymask.net"
echo "my domain name is : $DOMAIN_NAME"

# Update package lists
sudo apt-get update

# Install Certbot (if not already installed)
if [ ! -f "/usr/bin/certbot" ]; then
    sudo apt-get install -y certbot
fi

# Generate SSL certificate using Certbot (only if certificates don't exist)
if [ ! -d "/etc/letsencrypt/live/$DOMAIN_NAME" ]; then
    sudo certbot certonly --standalone -d $DOMAIN_NAME --email "714008556cjx@gmail.com" --agree-tos --no-eff-email
fi


# <!------ docker configuration -------!>

# install docker
curl -fsSL https://get.docker.com/ | sh

# Stop and remove all Docker containers
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)

# pull the latest docker image of the flask apps
sudo docker pull docker.io/jchenhsch/flask_app:latest

# Start the Flask in http 8000
sudo docker run -d  -p 8000:8000  --name flask_app1  jchenhsch/flask_app

# # Start your Flask app with Gunicorn and HTTPS on port 443
# sudo docker run -d -p 443:443 \
#   -v /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem \
#   -v /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem \
#   --name flask_app_https1 \
#   jchenhsch/flask_app_https:latest


# <!------ nginx configuration -------!>
sudo apt-get install nginx
sudo systemctl start nginx