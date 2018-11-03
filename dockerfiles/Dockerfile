FROM ubuntu:18.04

RUN apt-get update && apt-get install python3 python3-pip -y
RUN pip3 install gunicorn

WORKDIR /usr/src/app
COPY ../requirements.txt ./
COPY .. .
RUN pip3 install -r requirements.txt


CMD gunicorn -b 127.0.0.1:5000 --access-logfile - --error-logfile - blog:app

