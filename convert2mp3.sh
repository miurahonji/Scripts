#!/bin/bash

file="$1"
faad "$file"
lame "${file/.m4a/.wav}" "${file/.m4a/.mp3}"  
rm "${file/.m4a/.wav}" "$file" 
