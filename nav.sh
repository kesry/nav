#!/bin/bash -e

VERSION=v1.2.3
wget https://ghproxy.com/https://raw.githubusercontent.com/kesry/nav/$VERSION/Dockerfile \
&& docker build -t nav:$VERSION .

exit 0