FROM ubuntu:14.04

USER root
RUN apt-get update
RUN apt-get -y install python-software-properties
RUN apt-get -y install software-properties-common
RUN apt-get -y install libmysqlclient-dev
RUN apt-get -y install gcc make build-essential libssl-dev libffi-dev python-dev
RUN apt-get -y install python-pip
RUN pip install --upgrade pip


RUN mkdir -p /build
RUN cd /build
RUN mkdir -p /build/user_management_service
COPY . /build/user_management_service
WORKDIR /build/user_management_service
RUN pip install -r requirements.txt

ENV FLASK_CONFIGURATION=testing
EXPOSE 5000
