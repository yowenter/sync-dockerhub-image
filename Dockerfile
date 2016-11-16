FROM python:2.7.10-wheezy

MAINTAINER Taoge <wenter.wu@gmail.com>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN pip install  -r /usr/src/app/requirements.txt
COPY . /usr/src/app

CMD ["./consumer.sh"]