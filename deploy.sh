# Frontend on firebase
cd ./frontend/visualisation-site || exit
npm install
npm run build
firebase deploy
cd ../..

# Build backend
docker build --tag karelvb/bigdgroup27 .
docker push karelvb/bigdgroup27

# Backend on virtual wall
ssh groep36@193.191.169.46 "
sudo mkdir ~/data_trove
sudo mkdir ~/data_trove/raw
sudo mkdir ~/data_trove/tweetlength
sudo docker pull karelvb/bigdgroup27
sudo docker stop backend
sudo docker rm backend
sudo docker stop cronbackend
sudo docker rm cronbackend
sudo docker run --publish 80:80 -v ~/data_trove:/app/data_trove --detach --name backend karelvb/bigdgroup27
sudo docker run -v ~/data_trove:/app/data_trove --name cronbackend -it -d karelvb/bigdgroup27 /bin/bash
"

# TODO: put that in a cronjob
#sudo docker exec -it cronbackend bash -c \"cd /app && python ./data_collection_cron.py\"