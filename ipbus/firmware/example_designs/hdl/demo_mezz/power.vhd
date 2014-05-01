-- power.vhd
-- Mezzanine PicoBlaze
-- Jamieson Olsen <jamieson@fnal.gov>
-- 7 May 2013

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;

library unisim;
use unisim.vcomponents.all;

entity power is
port(
    clock : in std_logic;  -- 10MHz
    scl   : inout std_logic_vector(2 downto 0);
    sda   : inout std_logic_vector(2 downto 0));
end power;

architecture power_arch of power is

  component kcpsm6 
    generic(                 hwbuild : std_logic_vector(7 downto 0) := X"00";
                    interrupt_vector : std_logic_vector(11 downto 0) := X"3FF";
             scratch_pad_memory_size : integer := 64);
    port (                   address : out std_logic_vector(11 downto 0);
                         instruction : in std_logic_vector(17 downto 0);
                         bram_enable : out std_logic;
                             in_port : in std_logic_vector(7 downto 0);
                            out_port : out std_logic_vector(7 downto 0);
                             port_id : out std_logic_vector(7 downto 0);
                        write_strobe : out std_logic;
                      k_write_strobe : out std_logic;
                         read_strobe : out std_logic;
                           interrupt : in std_logic;
                       interrupt_ack : out std_logic;
                               sleep : in std_logic;
                               reset : in std_logic;
                                 clk : in std_logic);
  end component;

  component mezzanine                             
    generic(             C_FAMILY : string := "S6"; 
                C_RAM_SIZE_KWORDS : integer := 1;
             C_JTAG_LOADER_ENABLE : integer := 0);
    Port (      address : in std_logic_vector(11 downto 0);
            instruction : out std_logic_vector(17 downto 0);
                 enable : in std_logic;
                    rdl : out std_logic;                    
                    clk : in std_logic);
  end component;


signal         address  : std_logic_vector(11 downto 0);
signal     instruction  : std_logic_vector(17 downto 0);
signal     bram_enable  : std_logic;
signal         in_port  : std_logic_vector(7 downto 0);
signal        out_port  : std_logic_vector(7 downto 0);
signal         port_id  : std_logic_vector(7 downto 0);
signal    write_strobe  : std_logic;
signal  k_write_strobe  : std_logic;
signal     read_strobe  : std_logic;
signal       interrupt  : std_logic;
signal   interrupt_ack  : std_logic;
signal             rdl  : std_logic;
signal     int_request  : std_logic;
signal scl_reg, sda_reg : std_logic_vector(2 downto 0);
signal scl_mux, sda_mux : std_logic;
signal mux_reg          : std_logic_vector(1 downto 0);

begin

  processor: kcpsm6
    generic map (                 hwbuild => X"00", 
                         interrupt_vector => X"3FF",
                  scratch_pad_memory_size => 64)
    port map(      address => address,
               instruction => instruction,
               bram_enable => bram_enable,
                   port_id => port_id,
              write_strobe => write_strobe,
            k_write_strobe => k_write_strobe,
                  out_port => out_port,
               read_strobe => read_strobe,
                   in_port => in_port,
                 interrupt => interrupt,
             interrupt_ack => interrupt_ack,
                     sleep => '0',
                     reset => '0',
                       clk => clock);
 
  interrupt <= interrupt_ack;

  program_rom: mezzanine                         --Name to match your PSM file
    generic map(             C_FAMILY => "7S",   --Family 'S6', 'V6' or '7S'
                    C_RAM_SIZE_KWORDS => 2,      --Program size '1', '2' or '4'
                 C_JTAG_LOADER_ENABLE => 0)      --Include JTAG Loader when set to '1' 
    port map(      address => address,      
               instruction => instruction,
                    enable => bram_enable,
                       --rdl => reset,
                       clk => clock);

    scl_mux <= scl(0) when (mux_reg="00") else
               scl(1) when (mux_reg="01") else
               scl(2) when (mux_reg="10") else
               '0';

    sda_mux <= sda(0) when (mux_reg="00") else
               sda(1) when (mux_reg="01") else
               sda(2) when (mux_reg="10") else
               '0';

    inport_proc: process(clock)
    begin
    if rising_edge(clock) then

      case port_id(7 downto 0) is
        when X"01" => -- scl port
            in_port <= (scl_mux & "0000000");
        when X"02" => -- sda port
            in_port <= (sda_mux & "0000000");
        when others => 
            in_port <= X"00";
      end case;
    end if;
    end process inport_proc;

    outport_proc: process(clock)
    begin
        if rising_edge(clock) then
            if write_strobe = '1' then

                if (port_id(0) = '1') then  -- scl port 0x01
                   if (mux_reg="00") then
                      scl_reg(0) <= out_port(7);
                   elsif (mux_reg="01") then
                      scl_reg(1) <= out_port(7);
                   elsif (mux_reg="10") then
                      scl_reg(2) <= out_port(7);
                   end if;
                end if;

                if (port_id(1) = '1') then -- sda port 0x02 
                    if (mux_reg="00") then
                        sda_reg(0) <= out_port(7);
                    elsif (mux_reg="01") then
                        sda_reg(1) <= out_port(7);
                    elsif (mux_reg="10") then
                        sda_reg(2) <= out_port(7);
                    end if;
                end if;

                if (port_id(5) = '1') then -- mux port 0x20
                    mux_reg <= out_port(1 downto 0);
                end if;

            end if;
        end if; 
    end process outport_proc;

   scl(0) <= '0' when (scl_reg(0)='0') else 'Z';
   sda(0) <= '0' when (sda_reg(0)='0') else 'Z';

   scl(1) <= '0' when (scl_reg(1)='0') else 'Z';
   sda(1) <= '0' when (sda_reg(1)='0') else 'Z';

   scl(2) <= '0' when (scl_reg(2)='0') else 'Z';
   sda(2) <= '0' when (sda_reg(2)='0') else 'Z';

end power_arch;

