#!/bin/bash

USAGE='''
DOCUMENTATION:
--------------

EXAMPLES:
--------------
$ docker run -it rkx remove "$(cat config.yml|base64 -w 0)"
'''

if [ -z $1 ] || [ -z $2 ]; then
echo "$USAGE"
else
echo "$2" | base64 -d > /tmp/values.yml
ansible-playbook -v -e "devops_command=$1" /root/.ansible/playbook.yml
fi
