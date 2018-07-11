#!/bin/bash

cd tests
docker build -t oversea-cli .
cd ..

docker run --rm -ti -v `pwd`/..:/oversea --net=host oversea-cli $*
