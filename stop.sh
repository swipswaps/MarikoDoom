#!/bin/bash
# Obviously this is not the best way to stop the server/game but it works for now. 
# It will also kill all other unprivileged scripts though.

echo WARNING: This script also stops all unprivileged python scripts you are running.
read -n1 -p 'Do you want to continue? [y/N]: ' doit
case $doit in
  y|Y) echo && echo Stopping server... && killall python && killall python3 ;;
  n|N) echo && echo Abort. ;;
  *) echo && echo Abort. ;;
esac
