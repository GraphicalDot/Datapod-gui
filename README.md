


Docker usage
An IPFS docker image is hosted at hub.docker.com/r/ipfs/go-ipfs. To make files visible inside the container you need to mount a host directory with the -v option to docker. Choose a directory that you want to use to import/export files from IPFS. You should also choose a directory to store IPFS files that will persist when you restart the container.

export ipfs_staging=</absolute/path/to/somewhere/>
export ipfs_data=</absolute/path/to/somewhere_else/>
Start a container running ipfs and expose ports 4001, 5001 and 8080:
