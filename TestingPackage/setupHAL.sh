#!/bin/sh

export LD_LIBRARY_PATH=/opt/cactus/lib:$LD_LIBRARY_PATH
export PATH=/opt/cactus/bin:$PATH

source /home/ntran/Documents/myROOT/root/bin/thisroot.sh

export PYTHONDIR=/usr/bin/python
export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH
export PATH=$ROOTSYS/bin:$PATH