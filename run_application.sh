
#!/bin/bash 
#https://medium.com/@pigiuz/hw-accelerated-gui-apps-on-docker-7fd424fe813e
#https://stackoverflow.com/questions/20845056/how-can-i-expose-more-than-1-port-with-docker


#For exploring docker GUI on windows or mac
#http://somatorio.org/en/post/running-gui-apps-with-docker/


#http://wiki.ros.org/docker/Tutorials/GUI
#sudo docker build -t registry.gitlab.com/mesha/feynmen/feynmen_dnode:protoype -f DockerFiles/Dockerfile . 
sudo docker build -t feynmen_dnode:v1.0 -f DockerFiles/Dockerfile_feynmen . 


xhost +local:root
docker run -d --name feynmen_dnode -e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v /docker_data:/data/ipfs \
-p 8080:8080 -p 4001:4001 -p 127.0.0.1:5001:5001  -p 9001:9001 feynmen_prototype:v1.0


xhost +local:root; \
sudo docker run -it \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v /docker_data:/data/ipfs \
-p 8080:8080 -p 4001:4001 -p 127.0.0.1:5001:5001 -p 9001:9001 feynmen_prototype:v1.0 /bin/bash


sudo docker run -it \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw -h feynhost\
-v /docker_data:/data/ipfs --cpus=".5"  memory: 1024M
-p 8080:8080 -p 4001:4001 -p 127.0.0.1:5001:5001 -p 9001:9001 feynmen_prototype:v1.0 /bin/bash
