#!/usr/bin/env bash

set -ev

SCRIPT_DIR=$(dirname "$0")

if [[ -z "$GROUP" ]] ; then
    echo "Cannot find GROUP env var"
    exit 1
fi

if [[ -z "$COMMIT" ]] ; then
    echo "Cannot find COMMIT env var"
    exit 1
fi

if [[ "$(uname)" == "Darwin" ]]; then
    DOCKER_CMD=docker
else
    DOCKER_CMD="sudo docker"
fi
CODE_DIR=$(cd $SCRIPT_DIR/..; pwd)
echo $CODE_DIR

cp -r $CODE_DIR/cmd/ $CODE_DIR/docker/paymentsvc/cmd/
cp $CODE_DIR/*.go $CODE_DIR/docker/paymentsvc/

REPO=${GROUP}/$(basename payment);

$DOCKER_CMD build -t ${REPO}-dev $CODE_DIR/docker/paymentsvc;
$DOCKER_CMD create --name payment ${REPO}-dev;
$DOCKER_CMD cp payment:/app/main $CODE_DIR/docker/paymentsvc/app;
$DOCKER_CMD rm payment;
$DOCKER_CMD build -t ${REPO}:${COMMIT} -f $CODE_DIR/docker/paymentsvc/Dockerfile-release $CODE_DIR/docker/paymentsvc;
