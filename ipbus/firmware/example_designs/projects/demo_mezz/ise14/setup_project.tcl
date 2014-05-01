project new demo_mezz
project set family kintex7
project set device xc7k160t
project set package fbg484
project set speed -1

project set "Enable Multi-Threading" "2" -process "Map"
project set "Pack I/O Registers/Latches into IOBs" "For Inputs and Outputs" -process "Map"
project set "Enable Multi-Threading" "2" -process "Place & Route"
project set "Enable BitStream Compression" TRUE -process "Generate Programming File"

source $::env(REPOS_FW_DIR)/ipbus/firmware/example_designs/scripts/addfiles.tcl

project close
