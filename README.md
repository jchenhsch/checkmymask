# Mask Detection with Live Stream 
Live mask detection CNN webapp with dockerized setup and bootstrap script for GCP VM

## To set the entire app environment 

1. run bootstrap script by specify startup-script-url metadata and upload the script to Cloud Storage as url </br>
2. modify the default setting in the nginx to route both / location and /socket.io location/ of the traffic </br>
   and find the Ip address of docker image by using ifconfig </br>

   ```
   ## Sample mod for nginx default conf file /etc/nginx/sites-available/default
   
        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;
        location / {
                try_files $uri $uri/ =404;
                proxy_pass http://127.17.0.1:8000/;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_http_version 1.1;  # Add this line
                proxy_set_header Upgrade $http_upgrade;  # Add this line
                proxy_set_header Connection "upgrade";  # Add this line
                }
        location /socket.io/ {
        # Proxy WebSocket connections to the Flask app
                proxy_pass http://127.17.0.1:8000/socket.io/;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                 }
     ```
 3. access / test the website on domain https://checkmymask.net </br>
    should be able to see the processed images with face detected and "Mask" / "No Mask" annotation

## Improvements and current work
1. There are a lot of delays on image transmission of the live mask detection, and current the multiwork mode can only handle ***4*** concurrent requests at the same time. Need to set up either autoscaling or some load balancing features to make it more dynamic </br>

2. UI/UX experience needs improvement, maybe need more powerful models instead of just mask detection, login, logout, or some design on webpages need to be designed. (maybe react?) </br>



    
