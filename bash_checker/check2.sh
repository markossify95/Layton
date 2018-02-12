#!/bin/bash

DATA_DIR=../data/  # data directory location relative to this script
RS=$'\x1e'  # record separator
US=$'\x1f'  # field separator

function check_file()  # function for checking files
{
    file_name=$1  # first function parameter
    pattern=$2  # regex pattern
    file_path="$DATA_DIR$file_name"
    if [ -e ${file_path} ]; then
        line_count=`wc -l ${file_path} | cut -f1 -d' '`
        echo "$file_name found! Number of lines: $line_count"

        i=0  # line numbers
        err_lines=0
        while read LINE; do
            i=$((i+1))
            if ! [[ ${LINE} =~ $pattern ]]; then
                err_lines=$((err_lines+1))
                echo ${i}". line is in bad format! Content: " ${LINE}
            fi
        done < ${file_path}  # redirect file to loop (read)
        echo "WARNING: $err_lines lines are in incorrect format!"
    else
        echo "WARNING: required $file_name NOT found!"
    fi
}

check_file prefiksi.txt "[A-Z]{2}-[0-9]{3}[a-z]"
check_file PrefixNames_sr.properties "[A-Z0-9]{2}=(.)+"
check_file knjige.txt ".*${RS}200..${US}a.*"
