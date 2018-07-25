import re

def openFile(filename):
     originalfile=open(filename+'.txt')
     originitems=[]
     for line in originalfile.readlines():
          originitems.append(line)
     originalfile.close()
     return originitems

def reserveFile(filename,listname):
     revisedfile = open(filename+".txt",'w')
     revisedfile.writelines(listname)
     revisedfile.close()


#############################从这里开始################################3
hownet_words=openFile('howNetWord')
cilin_words=openFile('cilindata3')
raw_data=openFile('rawdata')
#hownet
A=[]
#cilin
B=[]
#hownet+cilin
C=[]
for each in raw_data:
     if (each in hownet_words) and (each in cilin_words):
          C.append(each)
     elif (each in hownet_words):
          A.append(each)
     elif (each in cilin_words):
          B.append(each)
reserveFile('A',A)
reserveFile('B',B)
reserveFile('C',C)
