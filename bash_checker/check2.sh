#!/bin/bash

DATA_DIR=../data/  # data directory location relative to this script
RS=$'\x1e'  # record separator
US=$'\x1f'  # field separator

function check_file()  # function for checking files
{
    file_name=$1  # first function parameter is file name
    pattern=$2  # second function parameter is regex pattern for file requirement
    file_path="$DATA_DIR$file_name"
    if [ -e ${file_path} ]; then
        line_count=`wc -l ${file_path} | cut -f1 -d' '`  # get total number of lines in a file
        echo "$file_name found! Number of lines: $line_count"

        i=0  # keep track of line numbers
        err_lines=0  # count number of lines with incorrect format
        while read LINE; do
            i=$((i+1))
            if ! [[ ${LINE} =~ $pattern ]]; then  # if line doesn't match pattern; then
                err_lines=$((err_lines+1))
                echo ${i}". line is in bad format! Content: " ${LINE}
            fi
        done < ${file_path}  # redirect file to loop (read)
        echo "WARNING: $err_lines lines are in incorrect format!"
    else
        echo "WARNING: required $file_name NOT found!"
    fi
}

check_file prefiksi.txt "[A-Z]{2}-[0-9]{3}[a-z]"  # checking "prefiksi" file
check_file PrefixNames_sr.properties "[A-Z]{2}=(.)+"  # checking "PrefixNames_sr" file
check_file knjige.txt ".*${RS}200..${US}a.*"  # checking "knjige" file