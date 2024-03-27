#!bin/bash
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
sudo systemctl start docker
sudo docker compose up -d
# chmod o+x docker-compose.yml runprogect.sh
