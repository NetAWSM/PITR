#!/bin/bash

DIR=/opt/bkpgsql





backup() {

pg_basebackup -h 127.0.0.1 -p5432 -U replicator  -D /opt/bkpgsql/$(date +\%d-\%m-\%y) --format=tar -Xs --progress --verbose 1> /var/log/backup/$(date +\%d-\%m-\%y).log 2> /var/log/backup/$(date +\%d-\%m-\%y).err

}

cp() {

  \cp /opt/bkpgsl/$(date +\%d-\%m-\%y) /opt/nw -R

}

delete() {

  rm -rf $DIR/*

}

case $1 in
        backup) backup;;
        cp) cp;;
        delete) delete;;
esac
