#!/bin/bash

DATA_DIR=../data/  # data directory location relative to this script

function check_file()
{
    file_name=$1
    pattern=$2
    file_path="$DATA_DIR$file_name"
    if [ -e ${file_path} ]; then
        line_count=`wc -l ${file_path} | cut -f1 -d' '`  # get total number of lines in a file
        echo "$file_name found! Number of lines: $line_count"

        i=0  # keep track of line numbers
        err_lines=0  # count number of lines with incorrect format
        while read LINE; do
            i=$((i+1))
            if ! [[ ${LINE} =~ ^($pattern)$ ]]; then
                err_lines=$((err_lines+1))
                echo ${i}". line is in bad format! Content: " ${LINE}
            fi
        done < ${file_path}
        echo "WARNING: $err_lines lines are in incorrect format!"
    else
        echo "WARNING: required $file_name NOT found!"
    fi
}

check_file "prefiksi.txt" "[A-Z]{2}-[0-9]{3}[a-z]"
#check_file "knjige.txt" "^(?!(*$'\x1e\x32\x30\x30'*)]" # ne radi
check_file "PrefixNames_sr.properties" "[A-Z]{2}=(.)+"