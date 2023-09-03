# 一个简单的导航

本次小版本更新，添加启用禁用支持，可以在list页面对当前数据禁用，也可以通过编辑禁用！。
同时，Dockerfile基础镜像修改，固定为3.18版本，不再以latest作为基础镜像！

## 本次内容更新
添加referrer

## 安装
版本v1.2.5

参考脚本
```shell
wget https://ghproxy.com/https://raw.githubusercontent.com/kesry/nav/v1.2.5/nav.sh && chmod +x nav.sh && ./nav.sh
```
 
以上脚本可以帮助你构建一个nav:v1.2.5的镜像。

你需要使用docker命令去启动它

```shell

sudo docker run -itd \
-p 9000:8080 \
-v ~/nav/db:/nav/db \
-v ~/nav/log:/nav/logs \
--name=nav \
nav:v1.2.5

```

```docker-compose.yml
  nav:
    image: nav:v1.2.5
    container_name: nav
    hostname: nav
    volumes:
      - /data/nav/db:/nav/db
      - /data/nav/log:/nav/logs
    environment: 
      - CONFIRM=kesry
      - LOG_LEVEL=error
    ports:
      - 80:8080
    restart: always  

```

默认服务验证码为:`kesry`