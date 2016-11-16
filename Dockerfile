FROM python:2.7.10-wheezy

MAINTAINER Taoge <wenter.wu@gmail.com>

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends libapparmor1 libsqlite3-0 libdevmapper1.02.1 curl ca-certificates libsystemd-journal0 libltdl7 && \
    ln -s /lib/x86_64-linux-gnu/libdevmapper.so.1.02.1 /usr/lib/x86_64-linux-gnu/libdevmapper.so.1.02 


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN pip install  -r /usr/src/app/requirements.txt
COPY . /usr/src/app

CMD ["sh","sync_docker/consumer.sh"]