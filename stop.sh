#!/bin/bash
# Obviously this is not the best way to stop the server/game but it works for now. 
# It will also kill all other unprivileged scripts though.

read -n1 -p 'Do you really want to stop the server? [y/N]: ' doit
case $doit in
  y|Y) echo && echo Stopping server... && pkill "vizdoom" && pkill "python server.py" && pkill "python3 server.py" ;;
  n|N) echo && echo Abort. ;;
  *) echo && echo Abort. ;;
esac
