#!/bin/bash


num_pipelineruns=${1:-10}

function run_pipeline {
    count=$1
    echo "#### Running $count PipelineRuns..."

    i=1
    while [ $i -le $count ];do
        oc create -f pipelinerun.yaml
        ((i++))
    done
}

function setup {
    oc apply -f tasks
    oc apply -f pipelines
}

# setup
run_pipeline $num_pipelineruns