#!/bin/bash
set -e
 
# If "-e uid={custom/local user id}" flag is not set for "docker run" command, use 9999 as default
CURRENT_UID=${uid:-9999}
 
# Notify user about the UID selected
echo "Current UID : $CURRENT_UID"
# Create user called "docker" with selected UID
useradd --shell /bin/bash -u $CURRENT_UID -o -c "" -m docker
# Set "HOME" ENV variable for user's home directory
export HOME=/home/docker
 
# Execute process
exec /usr/local/bin/gosu docker "$@"
