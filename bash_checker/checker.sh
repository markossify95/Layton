#!/bin/bash

file_name=prefiksi.txt

file_count=$(find ././../data/ -name prefiksi.txt | wc -l)

if [[ $file_count -gt 0 ]]; then
    echo "$file_name found!"
    lines=$(wc -l ././../data/$file_name)
    echo "Number of lines: " $lines
else
    echo "Warning: required $file_name NOT found!"
fi

file_name=knjige.txt

file_count=$(find ././../data/ -name $file_name | wc -l)

if [[ $file_count -gt 0 ]]; then
    echo "$file_name found!"
    lines=$(wc -l ././../data/$file_name)
    echo "Number of lines: " $lines
else
    echo "Warning: required $file_name NOT found!"
fi

file_name=PrefixNames_sr.properties

file_count=$(find ././../data/ -name $file_name | wc -l)

if [[ $file_count -gt 0 ]]; then
    echo "$file_name found!"
    lines=$(wc -l ././../data/$file_name)
    echo "Number of lines: " $lines
else
    echo "Warning: required $file_name NOT found!"
fi
