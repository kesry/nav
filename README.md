# 一个简单的导航

版本v1.1

参考脚本
```shell
wget https://ghproxy.com/https://raw.githubusercontent.com/kesry/nav/v1.1/nav.sh \
&& sudo chmod +x nav.sh && ./nav.sh
```

以上脚本可以帮助你构建一个nav:v1.1的镜像。

你需要使用docker命令去启动它

```shell

sudo docker run -itd -p 9000:8080 -v ~/nav/db:/nav/db -v ~/nav/log:/nav/log  --name=nav nav:v1.1

```