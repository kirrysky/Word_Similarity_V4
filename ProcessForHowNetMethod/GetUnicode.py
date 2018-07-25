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
# B=openFile('B')
C=openFile('C')
smalldict=openFile('smalldict-dict-8')
# all_words=B+C
all_words=C
result=[]

for each in smalldict:
     data=each.split(' ')
     if data[1] in all_words:
          result.append(each)

reserveFile('C-incilin',result)
