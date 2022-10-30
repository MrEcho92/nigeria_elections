
# stop any execution with non-zero status
set -ex
GIT_VERSION='git rev-parse --short @'
VERSION=${DEPLOY_VERSION:-$GIT_VERSION}

# args passed in ./scripts/deploy.sh <arg> 
# TEST=$1
# echo $TEST 

if [[$VIRTUAL_ENV == ""]]: 
then
    echo "Aborting... you are not in virtualenv."
fi

echo "Removing static build folder"
rm -rf ./static/*
echo "Generating django static files"
python ./manage.py collectstatic
echo "static files generated...done"

echo "GIT_VERISON: $GIT_VERSION VERSION: $VERSION "

echo "Deploying via Google App Engine"
gcloud app deploy --project=vision2023 --no-promote --version $VERSION
