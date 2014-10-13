#!/bin/sh
mkdir work

echo "Compiling Tri-Mode Ethernet MAC Core Simulation Models"
ncvhdl -v93 -work work ../../../tri_mode_eth_mac_v5_5.vhd

echo "Compiling Example Design"
ncvhdl -v93 -work work \
../../example_design/fifo/tri_mode_eth_mac_v5_5_tx_client_fifo.vhd \
../../example_design/fifo/tri_mode_eth_mac_v5_5_rx_client_fifo.vhd \
../../example_design/fifo/tri_mode_eth_mac_v5_5_ten_100_1g_eth_fifo.vhd \
../../example_design/common/tri_mode_eth_mac_v5_5_reset_sync.vhd \
../../example_design/common/tri_mode_eth_mac_v5_5_sync_block.vhd \
../../example_design/pat_gen/tri_mode_eth_mac_v5_5_address_swap.vhd \
../../example_design/pat_gen/tri_mode_eth_mac_v5_5_axi_mux.vhd \
../../example_design/pat_gen/tri_mode_eth_mac_v5_5_axi_pat_gen.vhd \
../../example_design/pat_gen/tri_mode_eth_mac_v5_5_axi_pat_check.vhd \
../../example_design/pat_gen/tri_mode_eth_mac_v5_5_axi_pipe.vhd \
../../example_design/pat_gen/tri_mode_eth_mac_v5_5_basic_pat_gen.vhd \
../../example_design/control/tri_mode_eth_mac_v5_5_config_vector_sm.vhd \
../../example_design/tri_mode_eth_mac_v5_5_block.vhd \
../../example_design/tri_mode_eth_mac_v5_5_fifo_block.vhd \
../../example_design/tri_mode_eth_mac_v5_5_example_design.vhd


echo "Compiling Test Bench"
ncvhdl -v93 -work work ../demo_tb.vhd

echo "Elaborating design"
ncelab -access +r work.demo_tb:behav

echo "Starting simulation"
ncsim -gui work.demo_tb:behav -input @"simvision -input wave_ncsim.sv"
