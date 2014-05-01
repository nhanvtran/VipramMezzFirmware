-- ipbus_vpram.vhd
-- VIPRAM Test Mezzanine TOP LEVEL
-- Jamieson Olsen <jamieson@fnal.gov>
-- 24 April 2014
--
-- there are a large number of registers and blockram ports to read
-- therefore the read/mux logic is pipelined over several stages
-- read latency is X clock cycles
--
-- this is the top level of the SLAVE interface
-- for use within the IPBus framework.  Addressing is 20 bits.
-- clock is used for reading/writing registers and buffers
-- clk200 is 200MHz and used for clocking out the vectors and 
-- calibrating the output delay taps.
--
-- Read and Write latency is TWO cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library unisim;
use unisim.vcomponents.all;

use work.mezzanine_package.all;
use work.ipbus.all;

entity ipbus_vpram is
port(
    -- IPBus signals
    clock:     in  std_logic;
    reset:     in  std_logic;
    ipbus_in:  in  ipb_wbus;
    ipbus_out: out ipb_rbus;

    -- Mezzanine Signals
    sysclk_p, sysclk_n: in std_logic;

    -- Mezzanine VIPRAM Signals
    VIPD: in std_logic_vector(31 downto 0);
    VIPQ: out std_logic_vector(83 downto 0);
    mc_a, mc_b: out std_logic;

    -- Mezzanine VIPRAM/Power Signals
    vpwr_en: out   std_logic;
    sda:     inout std_logic_vector(2 downto 0);
    scl:     inout std_logic_vector(2 downto 0));
end ipbus_vpram;

architecture rtl of ipbus_vpram is

    component ovec
    port(
        clock:  in  std_logic;
        addr:   in  std_logic_vector(9 downto 0);
        din:    in  std_logic_vector(31 downto 0);
        we:     in  std_logic;
        dout:   out std_logic_vector(31 downto 0);

        clk:    in  std_logic;
        reset:  in  std_logic;
        go:     in  std_logic;
        q:      out std_logic);
    end component;

    component ivec
    port(
        clock:  in  std_logic;
        addr:   in  std_logic_vector( 9 downto 0);
        dout:   out std_logic_vector(31 downto 0);
        clk:    in std_logic;
        reset:  in std_logic;
        go:     in std_logic;
        d:      in std_logic
        );
    end component;

    component mezz_clock2
    port
     (-- Clock in ports
      SYS_CLK_P         : in     std_logic;
      SYS_CLK_N         : in     std_logic;
      -- Clock out ports
      CLK          : out    std_logic;
      CLK_A        : out    std_logic;
      CLK_B        : out    std_logic;
      SLOW_CLK     : out    std_logic;
      -- Dynamic reconfiguration ports
      DADDR             : in     std_logic_vector( 6 downto 0);
      DCLK              : in     std_logic;
      DEN               : in     std_logic;
      DIN               : in     std_logic_vector(15 downto 0);
      DOUT              : out    std_logic_vector(15 downto 0);
      DWE               : in     std_logic;
      DRDY              : out    std_logic;
      -- Status and control signals
      RESET             : in     std_logic;
      LOCKED            : out    std_logic
     );
    end component;

    component power is
    port(
        clock   : in std_logic;  -- 10MHz
        scl     : inout std_logic_vector(2 downto 0);
        sda     : inout std_logic_vector(2 downto 0));
    end component;

    signal ovec_dout: array84x32;
    signal ivec_dout: array32x32;
    signal addr_reg, addr2_reg : std_logic_vector(19 downto 0);
    signal din_reg : std_logic_vector(31 downto 0);
    signal we_reg, go200_reg : std_logic;
    signal go_reg : std_logic_vector(1 downto 0);
    signal test_reg, ctrl_reg : std_logic_vector(31 downto 0);
    signal ack_reg: std_logic_vector(1 downto 0);
    signal ovec_we: std_logic_vector(83 downto 0);

    signal clk, clk_a, clk_b, slow_clk: std_logic;
    signal mmcm_den, mmcm_dwe, mmcm_locked, mmcm_drdy : std_logic;
    signal mmcm_dout : std_logic_vector(15 downto 0);

begin

-- clock control.  This module is driven by the 200MHz oscillator in the board.
-- the dynamic reconfig port enables the user to change the frequency and phase
-- of clk, clk_a, and clk_b.  
-- 
-- clk is the main clock used for driving the ovec and ivec modules
--
-- clk_a goes to the mc_a clock output, this clock should be the same frequency
--    as clk but with a 180 degree phase shift.  this shifts the rising edge
--    to the center of the output bit.
--
-- clk_b should be the same frequency as clk, but with a slightly larger phase 
--    shift, say, 190 degrees.  the time difference between mc_a and mc_b
--    generates the match-line-precharge in the VIPRAM chip 
--
-- slow clk is a constant 10MHz for the picoblaze processor
--
-- dynamic config port is a block of 128 16-bit registers

mmcm_inst: mezz_clock2
port map(
    SYS_CLK_P => sysclk_p,
    SYS_CLK_N => sysclk_n,
    CLK       => clk,
    CLK_A     => clk_a,
    CLK_B     => clk_b,
    SLOW_CLK  => slow_clk,

    DADDR     => addr_reg(6 downto 0),
    DCLK      => clock,
    DEN       => mmcm_den,
    DIN       => din_reg(15 downto 0),
    DOUT      => mmcm_dout(15 downto 0),
    DWE       => mmcm_dwe,
    DRDY      => mmcm_drdy,
    RESET     => ctrl_reg(0),  -- self clearing control bit
    LOCKED    => mmcm_locked);

mmcm_den <= '1' when std_match( addr_reg, MMCM_OFFSET ) else '0';
mmcm_dwe <= mmcm_den and we_reg;





-- register memory bus inputs

input_proc: process(clock)
begin
    if rising_edge(clock) then
        din_reg   <= ipbus_in.ipb_wdata;
        we_reg    <= ipbus_in.ipb_strobe and ipbus_in.ipb_write;
        addr_reg  <= ipbus_in.ipb_addr(19 downto 0);
        addr2_reg <= addr_reg;
    end if;
end process input_proc;

-- misc registers

reg_proc: process(clock)
begin
    if rising_edge(clock) then
        if (reset='1') then
            ctrl_reg <= (others=>'0');
            test_reg <= X"00000000";
            go_reg <= "00";
        else
            if (addr_reg=CONTROL_OFFSET and we_reg='1') then
                ctrl_reg <= din_reg(31 downto 0);
            else -- auto clear function
                ctrl_reg <= mmcm_locked & mmcm_drdy & "00" & X"0000000";
            end if;

            if (addr_reg=TESTREG_OFFSET and we_reg='1') then
                test_reg <= din_reg;
            end if;

            if (addr_reg=GOREG_OFFSET and we_reg='1') then
                go_reg(0) <= '1';
            else
                go_reg(0) <= '0';
            end if;

            go_reg(1) <= go_reg(0);  -- stretch 2 clks wide

        end if;
    end if;
end process reg_proc;

-- cross the clock domain on the go signal

go_proc: process(clock)
begin
    if rising_edge(clock) then
        if (reset='1') then
            go200_reg <= '0';
        elsif (go_reg(0)='1' or go_reg(1)='1') then
            go200_reg <= '1';
        else
            go200_reg <= '0';
        end if;
    end if;
end process go_proc;

-- write enables

wegen: for i in 83 downto 0 generate
    ovec_we(i)  <= '1' when ( we_reg='1' and std_match(addr_reg, OVEC_OFFSET(i)) ) else '0';
end generate;

-- 84 output vector modules, ram interface is R/W

sendgen: for i in 83 downto 0 generate
    ovec_inst: ovec
    port map(
        clock => clock,
        addr  => addr_reg(9 downto 0),
        din   => din_reg,
        dout  => ovec_dout(i),
        we    => ovec_we(i),

        clk    => clk,
        reset  => reset,
        go     => go200_reg,
        q      => VIPQ(i));
end generate;

-- 32 input vector modules, ram interface is RO

recgen: for i in 31 downto 0 generate
    ivec_inst: ivec
    port map(
        clock => clock,
        addr  => addr_reg(9 downto 0), -- 10 bit
        dout  => ivec_dout(i),         -- 32 bit

        clk    => clk,
        reset  => reset,
        go     => go200_reg,
        d      => VIPD(i)
    );
end generate recgen;

-- simple big giant mux to select everything... does this even fit?
-- note that the address constants may have don't cares in them
-- e.g. "10101-----1101" so std_match is required.

ipbus_out.ipb_rdata <=  
        ovec_dout( 0) when std_match(addr2_reg, OVEC_OFFSET( 0) ) else
        ovec_dout( 1) when std_match(addr2_reg, OVEC_OFFSET( 1) ) else
        ovec_dout( 2) when std_match(addr2_reg, OVEC_OFFSET( 2) ) else
        ovec_dout( 3) when std_match(addr2_reg, OVEC_OFFSET( 3) ) else
        ovec_dout( 4) when std_match(addr2_reg, OVEC_OFFSET( 4) ) else
        ovec_dout( 5) when std_match(addr2_reg, OVEC_OFFSET( 5) ) else
        ovec_dout( 6) when std_match(addr2_reg, OVEC_OFFSET( 6) ) else
        ovec_dout( 7) when std_match(addr2_reg, OVEC_OFFSET( 7) ) else
        ovec_dout( 8) when std_match(addr2_reg, OVEC_OFFSET( 8) ) else
        ovec_dout( 9) when std_match(addr2_reg, OVEC_OFFSET( 9) ) else

        ovec_dout(10) when std_match(addr2_reg, OVEC_OFFSET(10) ) else
        ovec_dout(11) when std_match(addr2_reg, OVEC_OFFSET(11) ) else
        ovec_dout(12) when std_match(addr2_reg, OVEC_OFFSET(12) ) else
        ovec_dout(13) when std_match(addr2_reg, OVEC_OFFSET(13) ) else
        ovec_dout(14) when std_match(addr2_reg, OVEC_OFFSET(14) ) else
        ovec_dout(15) when std_match(addr2_reg, OVEC_OFFSET(15) ) else
        ovec_dout(16) when std_match(addr2_reg, OVEC_OFFSET(16) ) else
        ovec_dout(17) when std_match(addr2_reg, OVEC_OFFSET(17) ) else
        ovec_dout(18) when std_match(addr2_reg, OVEC_OFFSET(18) ) else
        ovec_dout(19) when std_match(addr2_reg, OVEC_OFFSET(19) ) else

        ovec_dout(20) when std_match(addr2_reg, OVEC_OFFSET(20) ) else
        ovec_dout(21) when std_match(addr2_reg, OVEC_OFFSET(21) ) else
        ovec_dout(22) when std_match(addr2_reg, OVEC_OFFSET(22) ) else
        ovec_dout(23) when std_match(addr2_reg, OVEC_OFFSET(23) ) else
        ovec_dout(24) when std_match(addr2_reg, OVEC_OFFSET(24) ) else
        ovec_dout(25) when std_match(addr2_reg, OVEC_OFFSET(25) ) else
        ovec_dout(26) when std_match(addr2_reg, OVEC_OFFSET(26) ) else
        ovec_dout(27) when std_match(addr2_reg, OVEC_OFFSET(27) ) else
        ovec_dout(28) when std_match(addr2_reg, OVEC_OFFSET(28) ) else
        ovec_dout(29) when std_match(addr2_reg, OVEC_OFFSET(29) ) else

        ovec_dout(30) when std_match(addr2_reg, OVEC_OFFSET(30) ) else
        ovec_dout(31) when std_match(addr2_reg, OVEC_OFFSET(31) ) else
        ovec_dout(32) when std_match(addr2_reg, OVEC_OFFSET(32) ) else
        ovec_dout(33) when std_match(addr2_reg, OVEC_OFFSET(33) ) else
        ovec_dout(34) when std_match(addr2_reg, OVEC_OFFSET(34) ) else
        ovec_dout(35) when std_match(addr2_reg, OVEC_OFFSET(35) ) else
        ovec_dout(36) when std_match(addr2_reg, OVEC_OFFSET(36) ) else
        ovec_dout(37) when std_match(addr2_reg, OVEC_OFFSET(37) ) else
        ovec_dout(38) when std_match(addr2_reg, OVEC_OFFSET(38) ) else
        ovec_dout(39) when std_match(addr2_reg, OVEC_OFFSET(39) ) else

        ovec_dout(40) when std_match(addr2_reg, OVEC_OFFSET(40) ) else
        ovec_dout(41) when std_match(addr2_reg, OVEC_OFFSET(41) ) else
        ovec_dout(42) when std_match(addr2_reg, OVEC_OFFSET(42) ) else
        ovec_dout(43) when std_match(addr2_reg, OVEC_OFFSET(43) ) else
        ovec_dout(44) when std_match(addr2_reg, OVEC_OFFSET(44) ) else
        ovec_dout(45) when std_match(addr2_reg, OVEC_OFFSET(45) ) else
        ovec_dout(46) when std_match(addr2_reg, OVEC_OFFSET(46) ) else
        ovec_dout(47) when std_match(addr2_reg, OVEC_OFFSET(47) ) else
        ovec_dout(48) when std_match(addr2_reg, OVEC_OFFSET(48) ) else
        ovec_dout(49) when std_match(addr2_reg, OVEC_OFFSET(49) ) else

        ovec_dout(50) when std_match(addr2_reg, OVEC_OFFSET(50) ) else
        ovec_dout(51) when std_match(addr2_reg, OVEC_OFFSET(51) ) else
        ovec_dout(52) when std_match(addr2_reg, OVEC_OFFSET(52) ) else
        ovec_dout(53) when std_match(addr2_reg, OVEC_OFFSET(53) ) else
        ovec_dout(54) when std_match(addr2_reg, OVEC_OFFSET(54) ) else
        ovec_dout(55) when std_match(addr2_reg, OVEC_OFFSET(55) ) else
        ovec_dout(56) when std_match(addr2_reg, OVEC_OFFSET(56) ) else
        ovec_dout(57) when std_match(addr2_reg, OVEC_OFFSET(57) ) else
        ovec_dout(58) when std_match(addr2_reg, OVEC_OFFSET(58) ) else
        ovec_dout(59) when std_match(addr2_reg, OVEC_OFFSET(59) ) else

        ovec_dout(60) when std_match(addr2_reg, OVEC_OFFSET(60) ) else
        ovec_dout(61) when std_match(addr2_reg, OVEC_OFFSET(61) ) else
        ovec_dout(62) when std_match(addr2_reg, OVEC_OFFSET(62) ) else
        ovec_dout(63) when std_match(addr2_reg, OVEC_OFFSET(63) ) else
        ovec_dout(64) when std_match(addr2_reg, OVEC_OFFSET(64) ) else
        ovec_dout(65) when std_match(addr2_reg, OVEC_OFFSET(65) ) else
        ovec_dout(66) when std_match(addr2_reg, OVEC_OFFSET(66) ) else
        ovec_dout(67) when std_match(addr2_reg, OVEC_OFFSET(67) ) else
        ovec_dout(68) when std_match(addr2_reg, OVEC_OFFSET(68) ) else
        ovec_dout(69) when std_match(addr2_reg, OVEC_OFFSET(69) ) else

        ovec_dout(70) when std_match(addr2_reg, OVEC_OFFSET(70) ) else
        ovec_dout(71) when std_match(addr2_reg, OVEC_OFFSET(71) ) else
        ovec_dout(72) when std_match(addr2_reg, OVEC_OFFSET(72) ) else
        ovec_dout(73) when std_match(addr2_reg, OVEC_OFFSET(73) ) else
        ovec_dout(74) when std_match(addr2_reg, OVEC_OFFSET(74) ) else
        ovec_dout(75) when std_match(addr2_reg, OVEC_OFFSET(75) ) else
        ovec_dout(76) when std_match(addr2_reg, OVEC_OFFSET(76) ) else
        ovec_dout(77) when std_match(addr2_reg, OVEC_OFFSET(77) ) else
        ovec_dout(78) when std_match(addr2_reg, OVEC_OFFSET(78) ) else
        ovec_dout(79) when std_match(addr2_reg, OVEC_OFFSET(79) ) else

        ovec_dout(80) when std_match(addr2_reg, OVEC_OFFSET(80) ) else
        ovec_dout(81) when std_match(addr2_reg, OVEC_OFFSET(81) ) else
        ovec_dout(82) when std_match(addr2_reg, OVEC_OFFSET(82) ) else
        ovec_dout(83) when std_match(addr2_reg, OVEC_OFFSET(83) ) else

        ivec_dout( 0) when std_match( addr2_reg, IVEC_OFFSET( 0) ) else
        ivec_dout( 1) when std_match( addr2_reg, IVEC_OFFSET( 1) ) else
        ivec_dout( 2) when std_match( addr2_reg, IVEC_OFFSET( 2) ) else
        ivec_dout( 3) when std_match( addr2_reg, IVEC_OFFSET( 3) ) else
        ivec_dout( 4) when std_match( addr2_reg, IVEC_OFFSET( 4) ) else
        ivec_dout( 5) when std_match( addr2_reg, IVEC_OFFSET( 5) ) else
        ivec_dout( 6) when std_match( addr2_reg, IVEC_OFFSET( 6) ) else
        ivec_dout( 7) when std_match( addr2_reg, IVEC_OFFSET( 7) ) else
        ivec_dout( 8) when std_match( addr2_reg, IVEC_OFFSET( 8) ) else
        ivec_dout( 9) when std_match( addr2_reg, IVEC_OFFSET( 9) ) else
        ivec_dout(10) when std_match( addr2_reg, IVEC_OFFSET(10) ) else
        ivec_dout(11) when std_match( addr2_reg, IVEC_OFFSET(11) ) else
        ivec_dout(12) when std_match( addr2_reg, IVEC_OFFSET(12) ) else
        ivec_dout(13) when std_match( addr2_reg, IVEC_OFFSET(13) ) else
        ivec_dout(14) when std_match( addr2_reg, IVEC_OFFSET(14) ) else
        ivec_dout(15) when std_match( addr2_reg, IVEC_OFFSET(15) ) else
        ivec_dout(16) when std_match( addr2_reg, IVEC_OFFSET(16) ) else
        ivec_dout(17) when std_match( addr2_reg, IVEC_OFFSET(17) ) else
        ivec_dout(18) when std_match( addr2_reg, IVEC_OFFSET(18) ) else
        ivec_dout(19) when std_match( addr2_reg, IVEC_OFFSET(19) ) else
        ivec_dout(20) when std_match( addr2_reg, IVEC_OFFSET(20) ) else
        ivec_dout(21) when std_match( addr2_reg, IVEC_OFFSET(21) ) else
        ivec_dout(22) when std_match( addr2_reg, IVEC_OFFSET(22) ) else
        ivec_dout(23) when std_match( addr2_reg, IVEC_OFFSET(23) ) else
        ivec_dout(24) when std_match( addr2_reg, IVEC_OFFSET(24) ) else
        ivec_dout(25) when std_match( addr2_reg, IVEC_OFFSET(25) ) else
        ivec_dout(26) when std_match( addr2_reg, IVEC_OFFSET(26) ) else
        ivec_dout(27) when std_match( addr2_reg, IVEC_OFFSET(27) ) else
        ivec_dout(28) when std_match( addr2_reg, IVEC_OFFSET(28) ) else
        ivec_dout(29) when std_match( addr2_reg, IVEC_OFFSET(29) ) else
        ivec_dout(30) when std_match( addr2_reg, IVEC_OFFSET(30) ) else
        ivec_dout(31) when std_match( addr2_reg, IVEC_OFFSET(31) ) else

        ctrl_reg              when std_match( addr2_reg, CONTROL_OFFSET  ) else
        VERSION               when std_match( addr2_reg, FIRMWARE_OFFSET ) else
        IDENTITY              when std_match( addr2_reg, IDENTITY_OFFSET ) else
        test_reg              when std_match( addr2_reg, TESTREG_OFFSET  ) else
        (X"0000" & mmcm_dout) when std_match( addr2_reg, MMCM_OFFSET ) else
        X"00000000";

-- output of this module is NOT registered

ack_proc: process(clock)
begin
    if rising_edge(clock) then
        if (reset='1') then
            ack_reg <= "00";
        else
            if (ipbus_in.ipb_strobe='1' and ack_reg(1 downto 0)="00") then
                ack_reg(0) <= '1';
            else
                ack_reg(0) <= '0';
            end if;
            ack_reg(1) <= ack_reg(0);
        end if;
    end if;
end process ack_proc;

ipbus_out.ipb_err <= '0';
ipbus_out.ipb_ack <= ack_reg(1);

-- power control has no interface with ipbus (yet)

power_inst: power
port map(
    clock   => slow_clk,
    scl     => scl,
    sda     => sda);

vpwr_en <= '1';  -- regulators must be enabled before setting output voltage

-- output clocks

MC_A_inst : ODDR
port map(
	Q  => mc_a,
	C  => clk_a,
    CE => '1',
	D1 => '1', 
	D2 => '0',
    R  => '0', 
    S  => '0');

MC_B_inst : ODDR
port map(
	Q  => mc_b,
	C  => clk_b,
    CE => '1',
	D1 => '1', 
	D2 => '0',
    R  => '0',
    S  => '0');

end rtl;

