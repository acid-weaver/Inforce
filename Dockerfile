FROM python:3.11

RUN mkdir /home/app
WORKDIR /home/app

COPY . .
RUN pip3 install -r requirements.txt
