#!/bin/bash -e

VERSION=v1.1
wget https://ghproxy.com/https://raw.githubusercontent.com/kesry/nav/v1.1/Dockerfile \
&& sudo docker build -t nav:$VERSION .\
&& sudo docker run -itd -p 9000:8080 -v ./nav/db:/nav/db -v ./nav/log:/nav/log  --name=nav nav:$VERSION

exit 0