
*https://medium.com/@pigiuz/hw-accelerated-gui-apps-on-docker-7fd424fe813e
*https://stackoverflow.com/questions/20845056/how-can-i-expose-more-than-1-port-with-docker


For exploring docker GUI on windows or mac
*http://somatorio.org/en/post/running-gui-apps-with-docker/


*http://wiki.ros.org/docker/Tutorials/GUI

this command will create a docker container with the name feynmen_prototype with tag v1.0 from the 
file Dockerfile_feynmen present in Dockerfiles folder in the project directory.  

```
sudo docker build -t feynmen_prototype:v1.0 -f DockerFiles/Dockerfile_feynmen . 
``` 


Command to push docker image onto the gitlab registry 
```
sudo docker build -t registry.gitlab.com/mesha/feynmen/feynmen_dnode:protoype -f DockerFiles/Dockerfile . 
``` 



*if you want to run docker in detached mode, but still you want to login into the docker container with
```
docker start <containerid>
docker attach <containerid>

```
After logging into the container, intitialize ipfs with 

```
ipfs init 
```

This will generate ipfs config file in ~/.ipfs/config and you can also see that config file with 
```
ipfs config show
```
Then run this comand to start ipfs to interact with other perrs on the network
```
ipfs daemon&
```

NOw you can add anything on IPFs with command 
```
ipfs add <file_path>
```
This will map host GUI with docker GUI and run the docker container 

```
xhost +local:root
docker run -d --name feynmen_dnode -e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v /docker_data:/data/ipfs \
-v /var/run/docker.sock:/var/run/docker.sock:ro \ #
-v /proc:/feynmen/proc:ro \
-v /sys/fs/cgroup:/feynmen/sys/fs/cgroup:ro \
-p 8080:8080 -p 4001:4001 -p 127.0.0.1:5001:5001  -p 9001:9001 feynmen_prototype:v1.0
```


Running this command will directly loginto your docker containers created from th image feynmen_prototype:v1.0
```
xhost +local:root; \
sudo docker run -it \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v /docker_data:/data/ipfs \
-p 8080:8080 -p 4001:4001 -p 127.0.0.1:5001:5001 -p 9001:9001 feynmen_prototype:v1.0 /bin/bash
```


The repo also has a requirements.txt file whihc can be run if you want to start kivy app on your host rather then container.
The ubuntu packages required to install the kicy packages ar eas follows .
```
sudo apt-utils \
    build-essential \
    zlib1g-dev python3 python3-pip python3-setuptools \
    python3-kivy python-kivy-examples  python3-kivy-common python3-kivy-bin python3-opengl  libmtdev1   ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev python3-dev libsdl2-net-dev  libsdl2-gfx-dev
```

