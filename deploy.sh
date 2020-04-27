
# Frontend on firebase
cd ./frontend/visualisation-site || exit
firebase deploy
cd ../..

# Build backend
docker build --tag karelvb/bigdgroup27 .
docker push karelvb/bigdgroup27


# Backend on virtual wall
# shellcheck disable=SC2035
#scp -r -v out.tar groep36@193.191.169.46:~

ssh groep36@193.191.169.46 "sudo docker run --publish 80:80 --detach --name backend karelvb/bigdgroup27"
