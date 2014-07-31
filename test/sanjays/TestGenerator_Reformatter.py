#Sid
#for protoVIPRAM , Initial Hardcoded patterns Testing
#sidjos@gmail.com
#ntran@fnal.gov


import fileinput
import os
import random
import shutil
import sys
import ROOT
sys.path.append("Builder")
from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *
ROOT.gStyle.SetPalette(1);
from optparse import OptionParser
#----------------------------------------------------------


testName = raw_input("Input Test Name: ")
Decision="null"

if os.path.isdir("Generated_Tests/"+testName) : Decision=raw_input("test already exists , Delete old test ? (y/n)")

if Decision=="y": 
	shutil.rmtree("Generated_Tests/"+testName)
elif Decision=="n" :
	sys.exit("Test Already Exists / Re-Run Code ")
else:
	print "Generating New Test"	

os.system("mkdir "+"Generated_Tests/"+testName);

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


#Only Edit Here : 

# Available Classes to use :

#def initializeLoadPhase(self):
#def loadUniformPatterns(self, row, col, iVal, disableInputs = 1): fill every CAM in road with [,,,]
#def loadSinglePattern(self, row, col, iVal, disableInputs = 1): 
#def initializeRunPhase(self, logic = [1,1,1,1]):  majority logic settings [,,,] 
#def checkPattern(self, pattern, specificRow = 0): run mode, look for a single pattern [,,,]
#def readOutMode(self, logic = [-99,-99,-99,-99]):

#### TEST 3 100 MHz
#inputPattern = inputBuilder("Generated_Tests/"+testName+"/"+testName+".root");    
#inputPattern.initializeLoadPhase();
#inputPattern.loadUniformPatterns(9, 9, 27, 4); 
#inputPattern.loadUniformPatterns(9, 11, 37, 4); 
#inputPattern.loadUniformPatterns(9, 13, 47, 4); 
#inputPattern.initializeRunPhase( [1,0,0,0] ); 
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [27,27,27,27] ,9);
#inputPattern.checkPattern( [37,37,37,37] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [47,47,47,47] ,9);
#for i in range(20):
#    inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.initializeRunPhase( [1,0,0,0] );
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [27,27,27,27] ,9);
#inputPattern.checkPattern( [37,37,37,37] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [47,47,47,47] ,9);
#for i in range(20):
#    inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.close();

# TEST 3 logic

inputPattern = inputBuilder("Generated_Tests/"+testName+"/"+testName+".root");    
inputPattern.initializeLoadPhase();
inputPattern.loadUniformPatterns(9, 9, 27, 1); 
inputPattern.loadUniformPatterns(9, 11, 37, 1); 
inputPattern.loadUniformPatterns(9, 13, 47, 1); 

inputPattern.initializeRunPhase( [1,0,0,0] ); 
inputPattern.checkPattern( [27,27,27,27] ,9);
inputPattern.checkPattern( [37,37,37,37] ,9);
inputPattern.checkPattern( [47,47,47,47] ,9);
for i in range(4):
    inputPattern.checkPattern( [01,01,01,01] ,9);

inputPattern.initializeRunPhase( [0,1,0,0] ); 
inputPattern.checkPattern( [27,27,27,27] ,9);
inputPattern.checkPattern( [01,37,37,37] ,9);
inputPattern.checkPattern( [01,01,47,47] ,9);
for i in range(4):
    inputPattern.checkPattern( [01,01,01,01] ,9);

inputPattern.initializeRunPhase( [0,0,1,0] ); 
inputPattern.checkPattern( [27,27,27,27] ,9);
inputPattern.checkPattern( [01,37,37,37] ,9);
inputPattern.checkPattern( [01,01,47,47] ,9);
inputPattern.checkPattern( [01,01,47,01] ,9);
for i in range(4):
    inputPattern.checkPattern( [01,01,01,01] ,9);

inputPattern.doRowChecker( 7 );
inputPattern.doRowChecker( 8 );
inputPattern.doRowChecker( 9 );
inputPattern.readOutMode();
inputPattern.close();

#visualizer = inputVisualizer( inputPattern.getFilename() );
#visualizer.writeToText( "test.txt" );

  
#### TEST 4
#inputPattern = inputBuilder("Generated_Tests/"+testName+"/"+testName+".root");    
#inputPattern.initializeLoadPhase();
#inputPattern.loadSinglePattern(9, 5, [5,10,15,20]); 
#inputPattern.loadSinglePattern(9, 10, [25,30,35,40]); 
#inputPattern.loadSinglePattern(9, 15, [45,50,55,60]); 
#inputPattern.loadSinglePattern(9, 20, [65,70,75,80]); 
#inputPattern.loadSinglePattern(9, 25, [85,90,95,100]); 
#inputPattern.initializeRunPhase( [1,0,0,0] ); 
#inputPattern.checkPattern( [5,10,15,20] ,9);
#inputPattern.checkPattern( [25,30,35,40] ,9);
#inputPattern.checkPattern( [45,50,55,60] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.initializeRunPhase( [1,0,0,0] );
#inputPattern.checkPattern( [65,70,75,80] ,9);
#inputPattern.checkPattern( [85,90,95,100] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.checkPattern( [00,00,00,00] ,9);
#inputPattern.close();    
    
visuA = inputVisualizer( inputPattern.getFilename() );
visuA.textVisualizer();

visuA.writeToText("Generated_Tests/"+testName+"/"+testName+".txt"); # write outputs
visuA.writeToText("Generated_Tests/"+testName+"/"+testName+"_withExpectedOutputs.txt",True); # write outputs

shutil.copyfile("Generated_Tests/"+testName+"/"+testName+".txt" ,"Generated_Tests/"+ testName + "/inputPattern.txt" ) 
shutil.copyfile("TestGenerator_Reformatter.py","Generated_Tests/"+ testName+"/"+testName + ".py" ) 

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


### Reformat Input File and Generate vipram_rom.vhd file 

reformatInput=raw_input("Generate vipram_rom.vhd for test ? (y/n)")
if reformatInput=="n":
	sys.exit("inputPattern.txt generated for Test ")
	

if os.path.isfile("Generated_Tests/"+testName + "/vipram_rom.vhd"):
	os.remove("Generated_Tests/"+testName +"/vipram_rom.vhd")
  
if os.path.isfile("Generated_Tests/"+testName + "/temporary_file_pattern.txt"):
	os.remove("Generated_Tests/"+testName  + "/temporary_file_pattern.txt")        

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1    
    
def Replace_at_mark(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)
 
shutil.copyfile("Generated_Tests/"+testName +"/"+"inputPattern.txt", "temporary_file_pattern.txt" ) 
shutil.copyfile("Builder/template_vipram_rom.vhd", "temporary_VHDL_file.vhd" ) 

print "Number_of_lines in Input Pattern" , file_len("temporary_file_pattern.txt")
print "Number of lines in Template VHDL File " , file_len("temporary_VHDL_file.vhd")

for line in fileinput.input( "temporary_file_pattern.txt" , inplace=1):
    print "%s%s%s%s" % ('"',line[:-1],'",',"\n"),

num_of_lines_ip = file_len("temporary_file_pattern.txt")


#8192-1
for K in range(num_of_lines_ip, 8191):
	with open("temporary_file_pattern.txt", "a") as inputFile:
   		inputFile.write('"0000000000000000000000000000000000000000000000000000000000000000000000000000000000000",\n')	

f=open("temporary_file_pattern.txt")
replaceExp=f.read()

#print replaceExp

Replace_at_mark("temporary_VHDL_file.vhd","//ReplaceMe", replaceExp)


#print replaceExp
#shutil.copyfile("temporary_VHDL_file.vhd", "/Users/sidjos/Desktop/vipram_rom.vhd" )
 
shutil.copy("temporary_file_pattern.txt" ,"Generated_Tests/"+ testName +"/"+testName+"_reformattedText.txt") 
shutil.copy("temporary_VHDL_file.vhd" , "Generated_Tests/"+testName+"/vipram_rom.vhd")
shutil.copy("temporary_VHDL_file.vhd" , "Generated_Tests/"+testName+"/" + testName + "_vipram_rom.vhd")
#shutil.copy("temporary_VHDL_file.vhd" , "Mezzanine_Firmware_2013-05-14/src/vipram_rom.vhd")


print "Number_of_lines in Reformatted Pattern" , file_len("temporary_file_pattern.txt")
print "Number of lines in Generated VHDL File " , file_len("temporary_VHDL_file.vhd") 

os.remove("temporary_file_pattern.txt")
os.remove("temporary_VHDL_file.vhd")

print "\n vipram_rom.vhd created , End \n " 

    
    

