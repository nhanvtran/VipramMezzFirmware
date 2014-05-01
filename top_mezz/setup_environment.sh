#!/bin/sh

XILINX_ROOT=/opt/Xilinx/14.7/ISE_DS
export PATH=${XILINX_ROOT}/ISE/bin/lin64:${PATH}
export PATH=${XILINX_ROOT}/EDK/gnu/microblaze/lin64/bin:${PATH}

export XILINXD_LICENSE_FILE=2700@ppd-acme
export LM_LICENSE_FILE=2700@ppd-acme

export REPOS_FW_DIR=$PWD/../
export REPOS_BUILD_DIR=$REPOS_FW_DIR/ipbus/firmware/example_designs/projects/demo_mezz/ise14

source $XILINX_ROOT/settings64.sh