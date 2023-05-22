FROM python:alpine

MAINTAINER "ikiwi <ikiwicc@gmail.com>"

# 设置为中文，时区为北京时间，alpinelinux更换为阿里云镜像
ENV LANG=zh_CN.UTF-8 \
    TZ=Asia/Shanghai \
    PS1="\u@\h:\w \$ "
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.cloud.tencent.com/g' /etc/apk/repositories

# 安装需要运行的服务或命令
RUN apk add --no-cache bash curl nano wget net-tools tzdata zip  && \
    echo "echo 'Hello, Python in Alpine!'"

WORKDIR /opt/app
ADD . .
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple/ -U pip
RUN pip3 config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/
RUN pip install --upgrade pip && pip install .

# 设置容器的环境变量
ENV HOSTNAME='pandora'     \
    PANDORA_SENTRY='false' \
    PANDORA_CLOUD='true'   \
    PANDORA_SERVER='0.0.0.0:8080'

ENTRYPOINT ["./startup.sh"]
