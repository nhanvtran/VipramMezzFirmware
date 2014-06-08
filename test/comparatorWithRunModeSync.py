import os

if __name__ == '__main__':

    f1 = open('root/tmp1_i.txt','r');
    f2 = open('root/tmp1_f.txt','r');

    #find offset
    file1 = f1.read();
    file2 = f2.read();    

    list1 = file1.split()
    list2 = file2.split()

    runModeLine1 = -1;
    runModeLine2 = -1;
    for i in range(len(list1)-1):
        
        compL = "".join(['1']*32);
        compR = "".join(['0']*32);

        curout  = list1[i][1:33]
        nextout = list1[i+1][1:33]
        
        if curout == compL and nextout == compR: 
            runModeLine1 = i;
            break;

    for i in range(len(list2)-1):
        
        compL = "".join(['1']*32);
        compR = "".join(['0']*32);

        curout  = list2[i][:32]
        nextout = list2[i+1][:32]
        
        if curout == compL and nextout == compR: 
            runModeLine2 = i;
            break;

    shift = runModeLine2 - runModeLine1;
    print "------------------------"
    print "Welcome to comparator..."
    print "Output shift is ",shift
    mismatchCtr = 0;
    for i in range(runModeLine1,len(list1)):
        
        curline1 = list1[i];    
        curline2 = list2[i+shift];

        checkData = curline1[0];
        comp1 = curline1[1:33]
        comp2 = curline2[:32]

        if int(checkData) == 1:
            #if comp1 == comp2: print "match!"
            if comp1 != comp2: 
                print "no match for time slice: ", i+1, ", checkData = ", checkData;
                mismatchCtr += 1;
    print "There are", mismatchCtr,"mismatches!";
    print "------------------------";



