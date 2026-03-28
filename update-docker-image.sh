#First, login to docker hub
#docker login --username=$user_name

#Create image
docker build --network=host -t isoform-mapper .

#Tag (find your image id
docker tag isoform-mapper glygen/isoform-mapper:1.0.0

#Push
docker push glygen/isoform-mapper:1.0.0

