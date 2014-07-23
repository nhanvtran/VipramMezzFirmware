-- power.vhd
-- controls I2C regulators U3, U10, U11 LTC3447 
-- I2C ADC U16 LTC2991
-- 
-- 9 Jul 2014 JTO

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;

library unisim;
use unisim.vcomponents.all;

entity power is
port(
    clock : in std_logic;  -- 10MHz
    reset : in std_logic;

    scl   : inout std_logic_vector(2 downto 0);
    sda   : inout std_logic_vector(2 downto 0);

    dvdd : in std_logic_vector(7 downto 0); -- set the output voltage
    vdd  : in std_logic_vector(7 downto 0);
    vpre : in std_logic_vector(7 downto 0);

    stat: out std_logic_vector(15 downto 0);  -- LTC2991 registers
    idvdd, ivdd, ivpre: out std_logic_vector(15 downto 0);
    vdvdd, vvdd, vvpre: out std_logic_vector(15 downto 0);
    vcc: out std_logic_vector(15 downto 0);
    temp: out std_logic_vector(15 downto 0)
);
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

signal scl_reg, sda_reg, scl_mux, sda_mux : std_logic;
signal mux_reg : std_logic_vector(1 downto 0);
signal msb_reg: std_logic_vector(7 downto 0);

signal stat_reg, vcc_reg, temp_reg: std_logic_vector(15 downto 0);
signal idvdd_reg, ivdd_reg, ivpre_reg, vdvdd_reg, vvdd_reg, vvpre_reg: std_logic_vector(15 downto 0);

begin

  processor: kcpsm6
    generic map (  hwbuild => X"00", 
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
                     reset => reset,
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

    scl_mux <= '0' when (mux_reg="00" and scl(0)='0') else
               '0' when (mux_reg="01" and scl(1)='0') else
               '0' when (mux_reg="10" and scl(2)='0') else
               '1';

    sda_mux <= '0' when (mux_reg="00" and sda(0)='0') else
               '0' when (mux_reg="01" and sda(1)='0') else
               '0' when (mux_reg="10" and sda(2)='0') else
               '1';

    inport_proc: process(clock)
    begin
    if rising_edge(clock) then

      case port_id(7 downto 0) is
        when X"01" =>
            in_port <= "0000000" & scl_mux;
        when X"02" =>
            in_port <= "0000000" & sda_mux;
        when X"04" =>
            in_port <= dvdd;
        when X"05" =>
            in_port <= vdd;
        when X"06" =>
            in_port <= vpre;   
        when others => 
            in_port <= X"00";
      end case;

    end if;
    end process inport_proc;

    outport_proc: process(clock)
    begin
        if rising_edge(clock) then
            if (write_strobe = '1') then

              case port_id(7 downto 0) is
                when X"01" => -- scl port
                    scl_reg <= out_port(7);
                when X"02" => -- sda port
                    sda_reg <= out_port(7);
                when X"03" =>
                    mux_reg <= out_port(1 downto 0);

                when X"80" => stat_reg(7 downto 0)  <= out_port;
                when X"81" => stat_reg(15 downto 8) <= out_port;

                when X"8A" => vdvdd_reg(15 downto 8) <= out_port;
                when X"8B" => vdvdd_reg(7 downto 0)  <= out_port;

                when X"8C" => idvdd_reg(15 downto 8) <= out_port;
                when X"8D" => idvdd_reg(7 downto 0)  <= out_port;

                when X"8E" => vvdd_reg(15 downto 8) <= out_port;
                when X"8F" => vvdd_reg(7 downto 0)  <= out_port;

                when X"90" => ivdd_reg(15 downto 8) <= out_port;
                when X"91" => ivdd_reg(7 downto 0)  <= out_port;

                when X"92" => vvpre_reg(15 downto 8) <= out_port;
                when X"93" => vvpre_reg(7 downto 0)  <= out_port;

                when X"94" => ivpre_reg(15 downto 8) <= out_port;
                when X"95" => ivpre_reg(7 downto 0)  <= out_port;

                when X"9A" => temp_reg(15 downto 8) <= out_port;
                when X"9B" => temp_reg(7 downto 0)  <= out_port;

                when X"9C" => vcc_reg(15 downto 8)  <= out_port;
                when X"9D" => vcc_reg(7 downto 0)   <= out_port;

                when others => 
                    null;
              end case;

            end if;
        end if; 
    end process outport_proc;

   scl(0) <= '0' when (scl_reg='0' and mux_reg="00") else 'Z';
   sda(0) <= '0' when (sda_reg='0' and mux_reg="00") else 'Z';

   scl(1) <= '0' when (scl_reg='0' and mux_reg="01") else 'Z';
   sda(1) <= '0' when (sda_reg='0' and mux_reg="01") else 'Z';

   scl(2) <= '0' when (scl_reg='0' and mux_reg="10") else 'Z';
   sda(2) <= '0' when (sda_reg='0' and mux_reg="10") else 'Z';

   stat <= stat_reg;
   vcc  <= vcc_reg;
   temp <= temp_reg;

   vdvdd <= vdvdd_reg;
   idvdd <= idvdd_reg;

   vvdd <= vvdd_reg;
   ivdd <= ivdd_reg;

   vvpre <= vvpre_reg;
   ivpre <= ivpre_reg;

end power_arch;

