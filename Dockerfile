FROM alpine:latest

ENV LANG=zh_CN.UTF-8
ENV LANGUAGE=zh_CN:zh
ENV LC_ALL=zh_CN.UTF-8
ENV HOST=0.0.0.0
ENV CONFIRM="kesry"
ENV LOG_LEVEL="error"
ENV TZ=Asia/Shanghai
ENV VERSION=1.1
WORKDIR /
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
        apk update && apk add --no-cache tzdata python3 py3-pip wget && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple bottle && \
        wget https://ghproxy.com/https://github.com/kesry/nav/archive/refs/heads/v$VERSION.tar.gz && tar -xzvf nav-v$VERSION.tar.gz --exclude=Dockerfile --exclude=nav.sh && \
        rm -rf v$VERSION.tar.gz && mv nav-v$VERSION nav && \
    apk del wget py3-pip
WORKDIR /nav
EXPOSE 8080/tcp
CMD ["python3", "/nav/main.py"]
