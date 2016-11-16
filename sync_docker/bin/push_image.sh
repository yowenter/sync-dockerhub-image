set -x 

echo 'start pushing image:' $@
docker push $@
