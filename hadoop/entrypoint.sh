#!/bin/bash
set -e

mkdir -p /home/hduser/hdata/dfs/name
mkdir -p /home/hduser/hdata/dfs/data
mkdir -p /home/hduser/hadoop-logs

if [ ! -d /home/hduser/hdata/dfs/name/current ]; then
    hdfs namenode -format -force
fi

hdfs --daemon start namenode
hdfs --daemon start datanode
yarn --daemon start resourcemanager
yarn --daemon start nodemanager

sleep 5
jps
tail -F /dev/null
