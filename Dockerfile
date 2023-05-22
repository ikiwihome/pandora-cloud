FROM python:alpine

MAINTAINER "ikiwi <ikiwicc@gmail.com>"

# 设置为中文，时区为北京时间，alpinelinux更换为腾讯云镜像
ENV LANG=zh_CN.UTF-8 \
    TZ=Asia/Shanghai \
    PS1="\u@\h:\w \$ "
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.cloud.tencent.com/g' /etc/apk/repositories

# 安装需要运行的服务或命令
RUN apk add --no-cache bash curl nano wget net-tools tzdata zip  && \
    echo "echo 'Hello, Python in Alpine!'"

# 设置当前工作文件夹为/opt/app
WORKDIR /opt/app

# 将当前目录全部拷贝到容器/opt/app文件夹中
ADD . .

# pip源更换为腾讯云镜像
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple/ -U pip
RUN pip3 config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/

# 最重要的这个安装命令
RUN pip install --upgrade pip && pip install .

# 设置容器的环境变量
ENV HOSTNAME='pandora'     \
    PANDORA_SENTRY='false'

ENTRYPOINT ["./startup.sh"]
