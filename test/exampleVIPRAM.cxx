#include <iostream>
#include "uhal/uhal.hpp"


using namespace uhal;

int main()
{
  try
  {
    setLogLevelTo(uhal::Error());  // Maximise uHAL logging
    // setLogLevelTo(uhal::Fatal());  // Minimise uHAL logging

    HwInterface hw = ConnectionManager::getDevice ( "Board1", "ipbusudp-2.0://192.168.0.131:50001","file:///home/sergo/IPBus/vipram_address.xml" );

    ValWord<uint32_t> result_i = hw.getNode ("VipMEM.Ident").read(); 
    //    hw.dispatch();                                                                                               
    ValWord<uint32_t> result_v = hw.getNode ("VipMEM.FWver").read(); 
    hw.dispatch();                                                                                               
    std::cout << "Read Identity:"<< std::hex << result_i.value() << " and firmware version"<<
      result_v.value()<<std::dec <<std::endl;

    hw.getNode ("VipMEM.TestReg").write(0xcafebabe);

    ValWord<uint32_t> result = hw.getNode ("VipMEM.TestReg").read();
    hw.dispatch();
    std::cout << "Test register contains the value: 0x" << std::hex << result.value() << std::dec <<std::endl;


    //fill a vector with random information
           const size_t N=1024;
           std::vector<uint32_t> xx;
	   for(size_t i=0; i!= N; ++i) xx.push_back(static_cast<uint32_t>(rand()));
	   hw.getNode ("VipMEM.D0").writeBlock(xx);
	   hw.dispatch();

	   //read back the information
	   ValVector< uint32_t > mem = hw.getNode ( "VipMEM.D0" ).readBlock (N);
	   hw.dispatch();

	   //	   If there is a single client we should read back the same informaiton
	   int mismatch_count=0;
	   for(size_t i=0; i!= N; ++i)
	     {
	       std::cout<< xx[i] <<"     "<< mem[i] <<"\n";
	       if (xx[i]!=mem[i]) mismatch_count++;
                 }
   
	   std::cout<<"Error rate ="<<mismatch_count/N*100<<"% \n";
  }



  catch ( const std::exception& e )
  {
		std::cout << "Something went wrong: " << e.what() << std::endl;
  }
  return 0;
}

