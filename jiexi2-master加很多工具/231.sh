#!/usr/bin/env bash


#!/bin/bash
IFS=' '
arr=${1}
#for v in ${arr[@]}
for v in $arr
do
echo "$v"
done