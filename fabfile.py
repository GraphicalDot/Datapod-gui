




from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager
from fabric.api import settings
env.warn_only = True # if you want to ignore exceptions and handle them yurself

env.use_ssh_config = True
env.hosts = ['192.168.1.15']
env.user = 'vagrant'
env.colorize_errors = True
#env.key_filename = '/home/feynman/VirtualMachines/.vagrant/machines/fubuntuone/virtualbox/private_key'
env.key_filename = '/home/feynman/VirtualMachines/.vagrant/machines/fubuntuone/virtualbox/private_key'


env.directory = '/home/vagrant/feynmen-base'
env.activate = 'source %s/bin/activate'%env.directory
env.home_directory = "/home/vagrant"



@_contextmanager
def virtualenv():
    with cd(env.directory), prefix(env.activate):
        yield




##this function shouldnt be use, We dont have any use of IPFS cluster and its now experimental, 
##instead we should use IPFS private or IPFs pub sub
def ipfs_cluster():
    run("wget https://dist.ipfs.io/ipfs-cluster-service/v0.4.0-rc1/ipfs-cluster-service_v0.4.0-rc1_linux-amd64.tar.gz")
    run("tar xvzf ipfs-cluster-service_v0.4.0-rc1_linux-amd64.tar.gz")
    run("rm ipfs-cluster-service_v0.4.0-rc1_linux-amd64.tar.gz")
    run("sudo mv ipfs-cluster-service/ipfs-cluster-service /usr/local/bin")
    run("rm -rf ipfs-cluster-service")
    """
    run("wget https://dist.ipfs.io/ipfs-cluster-ctl/v0.3.5/ipfs-cluster-ctl_v0.3.5_linux-amd64.tar.gz")
    run("tar xvfz ipfs-cluster-ctl_v0.3.5_linux-amd64.tar.gz")
    run("rm ipfs-cluster-ctl_v0.3.5_linux-amd64.tar.gz")
    run("sudo mv ipfs-cluster-ctl/ipfs-cluster-ctl /usr/local/bin")
    run("rm -rf ipfs-cluster-ctl")
    """



def python_packages():
    with virtualenv():
        run("pip freeze") 
        run('pip install -r requirements.txt')


def install_packages():
    run("sudo apt-get -y update")
    run("sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common\
            libpq-dev python-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libssl-dev libffi-dev\
            g++ python3-dev wget curl git python-pip python3-setuptools python3 python-dev python3-dev build-essential\
            libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev")

    run("sudo apt-get install ffmpeg \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libportmidi-dev \
        libswscale-dev \
        libavformat-dev \
        libavcodec-dev")


    #run("sudo easy_install3 pip")
    #run("sudo pip3 install --upgrade pip wheel setuptools")
    run("echo 'alias python=python3' >> ~/.bashrc")
    run("sudo pip install virtualenv")


def install_git_venv():
    with cd(env.home_directory):
        run("git clone https://github.com/kaali-python/feynmen-base.git")
    with cd(env.directory):
        run("virtualenv -p python3 .")


def install_go():
    """
    run("sudo curl -O https://storage.googleapis.com/golang/go1.9.1.linux-amd64.tar.gz")
    run("sudo tar -xvf go1.9.1.linux-amd64.tar.gz")
    with hide('output'):
        run("sudo mv go /usr/local")
    run("echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc")
    #run("exec bash")
    with settings(warn_only=True):
        run("go version") ##this could fail 
    """
    run("sudo apt install golang -y")
    run("'echo GOROOT=/usr/lib/go' >> ~/.bashrc")
    run("'echo GOPATH=$HOME/go' >> ~/.bashrc")
    run("'echo PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> ~/.bashrc")



def install_other():
    run('source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list')
    run('wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -')
    run('sudo apt-get update -y')
    run('sudo apt-get -y install rethinkdb')

    ##installing docker
    run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
    run("sudo apt-key fingerprint 0EBFCD88")
    run('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu zesty stable"')
    run("sudo apt-get -y update")
    run("sudo apt-get -y install docker-ce")
    run("sudo service docker start")


    ##installing docker-compose
    run('sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose')
    run('sudo chmod +x /usr/local/bin/docker-compose')
    run('echo "This is the docker compose version"')
    run('sudo docker-compose --version')



def install_ipfs():

    run('wget https://dist.ipfs.io/go-ipfs/v0.4.15/go-ipfs_v0.4.15_linux-amd64.tar.gz')
    #run('wget https://s3.ap-south-1.amazonaws.com/feynmenpublic/go-ipfs_v0.4.15_linux-amd64.tar.gz')
    run('tar xvfz go-ipfs_v0.4.15_linux-amd64.tar.gz')
    with cd('go-ipfs'):
        run("sudo ./install.sh")
        run("sudo apt-get -y install fuse") 
        with settings(warn_only=True):
            result = run("sudo groupadd fuse")
            if result.return_code == 0: 
                run("sudo usermod -aG fuse $(whoami)")
            else: 
                print ("Fuse user already exists")

    run("ipfs init")
    ##this changes dafualt port of IPFs from 8080 to 9001
    run("ipfs daemon&")
    run("ipfs swarm peers")
    run("cat ~/.ipfs/config")

    ##these two lines are very important as these are needed foir the 
    ## nodes on communicate on local network. 
    run("ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/9001")
    run("ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001")
    run("ipfs config --json Experimental.FilestoreEnabled true")

And then pass the --nocopy flag when running ipfs add


# python transactions.py --settings=project_settingss
def install_bigchaindb():
    ##delete pkg_resource from the requirements.txt file

    ##this is because the error
    ## Cannot uninstall 'PyYAML'. It is a distutils installed project and thus we cannot 
    ##accurately determine which files belong to it which would lead to only a partial uninstall.


    #rm -r /usr/lib/python2.7/dist-packages/chardet

    with virtualenv():
        #run("pip uninstall pyyaml")
        #run("sudo apt-get install libyaml-dev libpython3.5-dev")
        #run("sudo pip install pyyaml")
        ##run("pip install --ignore-installed pyyaml")
        run("sudo pip install --ignore-installed bigchaindb")
        run("pip install bigchaindb-driver")
       
    run("rethinkdb --daemon")
    run("bigchaindb -y configure rethinkdb")
    run("bigchaindb start&")
    ##If the content is not available locally, THe ipfs will download the content
    ## and store it locally.
    run(" ipfs cat /ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme")
    #run("bigchaindb set-replicas 3")


def install_sawtooth():

    ##installing sawtooth-core, and bringing up hyperledger sawtooth docker containers
    run("wget https://sawtooth.hyperledger.org/docs/core/releases/1.0.1/app_developers_guide/sawtooth-default.yaml")
    run("sudo docker-compose -f sawtooth-default.yaml up -d")



def deploy():
    install_packages()
    install_go()
    install_git_venv()
    python_packages()
    install_other()
    install_ipfs()
    install_bigchaindb()
    install_sawtooth()
    #ipfs_cluster()
    ##commands you need to run yourself
    run("ipfs daemon&")




def host_type():
        run('uname -s')

