import os

if __name__ == '__main__':

    f1 = open('root/tmp1_i.txt','r');
    f2 = open('root/tmp1_f.txt','r');

    lastline = "blah"
    ctr = 0;
    while True:

        curline1 = f1.readline().rstrip('\n')
        curline2 = f2.readline().rstrip('\n')

        # eof
        if curline1 == "" and curline2 == "": break;

        checkData = curline1[0];
        comp1 = curline1[1:]
        comp2 = curline2

        if int(checkData) == 1:
            print "time slice: ", ctr, ", checkData = ", checkData;
            print comp1
            print comp2
            if comp1 == comp2: print "match!"
            else: print "no match!"
        
        ctr += 1


