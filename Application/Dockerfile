FROM ubuntu:bionic
MAINTAINER Graphicaldot houzier.saurav@gmail.com

RUN apt-get -y update
RUN apt-get install -y software-properties-common build-essential
RUN  add-apt-repository ppa:deadsnakes/ppa
RUN  apt update
RUN  apt install -y  python3.6
RUN apt-get install -y python-setuptools python-pygame python-opengl
RUN apt-get install -y python-gst-1.0 python-enchant gstreamer1.0-plugins-good python-dev
RUN apt-get install -y  build-essential libgl1-mesa-dev libgles2-mesa-dev zlib1g-dev python-pip

RUN apt-get -y install apt-transport-https ca-certificates curl \
            libpq-dev python-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libssl-dev libffi-dev\
            g++ python3-dev wget curl git python-pip python3-setuptools python3 python-dev python3-dev\
            libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev

RUN apt-get install -y python3-pip

RUN alias python=python3.6

RUN pip3 install Cython==0.25.2 kivy-garden faker
WORKDIR /home/developer 
COPY requirements.txt  .
RUN pip3 install -r requirements.txt 
COPY . .



#RUN cd && git clone git://github.com/kivy/kivy.git
#RUN cd && cd kivy && make
#RUN cd && cd kivy && make install
RUN apt-get install  -y cython3

RUN cython3 --embed -o app.c latest.py
RUN gcc -Os -I /usr/include/python3.6m -o app app.c -lpython3.6m -lpthread -lm -lutil -ldl
RUN mkdir -p /home/build
RUN cp app /home/build
