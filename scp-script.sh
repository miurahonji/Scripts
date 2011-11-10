#!/bin/bash

SERVER=""
mode="receive"

usage(){
	echo "USAGE: ${0} server path [send/receive]"
	exit 0
}

test -z "$1" && usage
test -z "$2" && usage

case "$1" in
	quasar) 
		SERVER="quasar.las.ic.unicamp.br:~/" 
		USER="roberto" ;;
	pulsar) 
		SERVER="pulsar.itautec.inovasoft.unicamp.br:~/"
		USER="roberto" ;;
	everest) 
		SERVER="www.las.ic.unicamp.br:~/" 
		USER="roberto" ;;
	hub1) 
		SERVER="mcpkjhub1.ltc.austin.ibm.com:~/" 
		USER="honji" ;;
	dev1) 
		SERVER="mcpkjdev1.ltc.austin.ibm.com:~/" 
		USER="honji" ;;
	abat)
		SERVER="mcpabat.ltc.austin.ibm.com:/home/rmhonji/"
		USER="root" ;;
	*) 
		echo "Server $1 not found"
		exit 1 ;;
esac

__PATH__="$2"

test "$3" == "send" && {
	scp -r ${__PATH__} ${USER}@${SERVER} && echo "Stored at ${SERVER}"
	exit ${?}
}

STORE="/tmp/$1"
mkdir -p ${STORE}
scp -r $USER@${SERVER}:${__PATH__} ${STORE} && echo "Stored at ${STORE}"
exit ${?}
