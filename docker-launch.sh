BUILD_OPTION=""

if [ "$1" == "build" ]; then
  BUILD_OPTION="--build"
fi

docker-compose down
docker-compose up db -d
sleep 2
docker-compose up backend $BUILD_OPTION
