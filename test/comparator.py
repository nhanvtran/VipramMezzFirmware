import os

if __name__ == '__main__':

    f1 = open('tmp1_i.txt','r');
    f2 = open('tmp1_f.txt','r');

    lastline = "blah"
    ctr = 0;
    while not lastline == "":
        curline1 = f1.readline().rstrip('\n')
        curline2 = f2.readline().rstrip('\n')
        print ctr
        print curline1
        print " "+curline2
        ctr += 1
        lastline = curline1

