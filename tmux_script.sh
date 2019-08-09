#!/bin/bash

#Create a new Detached Session
tmux new -d -s foo

#Execute the command in the Detached Session
tmux send-keys -t foo.0 "echo 'Hello $USER'" ENTER

tmux new -ds foo2

tmux send-keys -t foo2.0 "echo $TERM" ENTER

#Attach to the Session
#tmux a -t foo
