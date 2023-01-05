#!/bin/bash

pr_list=$(tkn pr list --no-headers | awk '{print $NF}')

pending=0
running=0
completed=0

for p in $pr_list; do
    if [[ "$p" == "---" ]]; then
        ((pending++))
    elif [[ "$p" == "Running" ]]; then
        ((running++))
    elif [[ "$p" == "Succeeded" ]]; then
        ((completed++))
    else
        echo "Unknown status: $p"
    fi
done


echo "Pending: $pending"
echo "Running: $running"
echo "Completed: $completed"
