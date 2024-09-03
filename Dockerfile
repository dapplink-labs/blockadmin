FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /blockadmin

RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

COPY ./blockadmin /blockadmin
RUN pip install -r requirements.txt
