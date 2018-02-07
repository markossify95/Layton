#!/bin/bash


file_name=prefiksi.txt
file_count=$(find ././../data/ -name prefiksi.txt | wc -l)

if [[ ${file_count} -gt 0 ]]; then
    echo "$file_name found!"
    lines=$(wc -l ././../data/${file_name})
    echo "Number of lines: " ${lines}
    set -f          # disable globing
    i=0
    lc=0
    for line in $(cat ././../data/${file_name}); do
        lc=$[lc+1]
        if ! [[ ${line} =~ ^[A-Z]{2}-[0-9]{3}[a-z]$ ]]; then
            i=$[i+1]
            echo ${lc}". line not ok: " ${line}
        fi
    done
    echo ${i} " lines are in bad format."
else
    echo "Warning: required $file_name NOT found!"
fi

file_name=knjige.txt
file_count=$(find ././../data/ -name ${file_name} | wc -l)

if [[ ${file_count} -gt 0 ]]; then
    echo "$file_name found!"
    lines=$(wc -l ././../data/${file_name})
    echo "Number of lines: " ${lines}
    IFS=$'\n'       # make newlines the only separator
    set -f          # disable globing
    i=0
    lc=0
    for line in $(cat ././../data/${file_name}); do
        lc=$[lc+1]
        if  [[ ${line} != *$'\x1e\x32\x30\x30'* ]]; then
            i=$[i+1]
            echo ${lc}". line not ok: " ${line}
        fi
    done
    echo ${i} " books are missing title [200]"
else
    echo "Warning: required $file_name NOT found!"
fi

file_name=PrefixNames_sr.properties
file_count=$(find ././../data/ -name ${file_name} | wc -l)

if [[ ${file_count} -gt 0 ]]; then
    echo "$file_name found!"
    lines=$(wc -l ././../data/${file_name})
    echo "Number of lines: " ${lines}
    set -f          # disable globing
    i=0
    lc=0
    for line in $(cat ././../data/${file_name}); do
        lc=$[lc+1]
        if ! [[ ${line} =~ ^[A-Z]{2}=(.)+$ ]]; then
            i=$[i+1]
            echo ${lc}". line not ok: " ${line}
        fi
    done
    echo ${i} " lines are in bad format."
else
    echo "Warning: required $file_name NOT found!"
fi
