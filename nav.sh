#!/bin/bash -e

VERSION=v1.2
wget https://ghproxy.com/https://raw.githubusercontent.com/kesry/nav/$VERSION/Dockerfile \
&& sudo docker build -t nav:$VERSION .
#&& sudo docker run -itd -p 9000:8080 -v ./nav/db:/nav/db -v ./nav/log:/nav/log  --name=nav nav:$VERSION

exit 0