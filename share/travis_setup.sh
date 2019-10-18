#!/bin/bash
set -evx

mkdir ~/.swampcore

# safety check
if [ ! -f ~/.swampcore/.swamp.conf ]; then
  cp share/swamp.conf.example ~/.swampcore/swamp.conf
fi
