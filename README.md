# 一个简单的导航

## 内容更新
1. 用户体验优化，域名默认公网，其余默认内网。
2. 在管理页面的列表中，除了base64外，悬浮显示内容。
3. 点击编号进入编辑界面。
4. 代码优化
## 安装
版本v1.2

参考脚本
```shell
wget https://ghproxy.com/https://raw.githubusercontent.com/kesry/nav/v1.2/nav.sh && sudo chmod +x nav.sh && ./nav.sh
```

以上脚本可以帮助你构建一个nav:v1.2的镜像。

你需要使用docker命令去启动它

```shell

sudo docker run -itd \
-p 9000:8080 \
-v ~/nav/db:/nav/db \
-v ~/nav/log:/nav/logs \
--name=nav \
nav:v1.2

```

```docker-compose.yml
  nav:
    image: nav:v1.2
    container_name: nav
    hostname: nav
    volumes:
      - /data/nav/db:/nav/db
      - /data/nav/log:/nav/logs
    environment: 
      - CONFIRM=orgic
      - LOG_LEVEL=error
    ports:
      - 80:8080
    restart: always  

```

默认服务验证码为:`kesry`