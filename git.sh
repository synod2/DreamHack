#! /bin/bash

msg="$(date '+%m')$(date '+%d')_master"

git add .
git commit -m $msg 
git push -u origin master
