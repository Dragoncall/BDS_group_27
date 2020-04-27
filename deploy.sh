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
ssh groep36@193.191.169.46 "sudo mkdir ~/data_trove
sudo docker stop backend
sudo docker rm backend
sudo docker run --publish 80:80 --detach --name backend karelvb/bigdgroup27 -v ~/data_trove:/app/data_trove
"
