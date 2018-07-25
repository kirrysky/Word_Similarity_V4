from hownet.howNet2 import *
from cilin.ciLin3 import *

#########################HowNet部分############################
### 打开WordFile
def openWordFile(filename):
    rawdata=[]
    rdf=open(filename)
    for line in rdf.readlines():
        rawdata.append(line[0:-1])
    rdf.close()
    return rawdata

### Track the process, let people know the process ###
###查看进度，有一定的进度条条，参数为文件名
###写入数据到文件中
def processTrackInHowNet(rawdata,filename):
    sim_dict = {}
    n=0
    for w1 in rawdata:
        result=open(filename,'a')
        rank_dict=GetResult(w1)
        result.write("========================================\n")
        ### 写入这个单词
        result.write(w1+":\n")
        ### 写入其相关词
        if len(rank_dict[0])==0:
            result.write("{}\n")
        else:

            for each in rank_dict:
                result.write(str(each[0])+"\t"+str(each[1])+"\n")
        result.write("========================================\n")
        sim_dict[w1]=rank_dict
        n+=1
        ### 显示进度
        print("完成了"+str((n/len(rawdata))*100)+"%!")
        result.close()

### 获取result #####
def GetResult(w1):
    global code2fatherDict
    global score
    ### 用字典法进行速度的提升
    howNetWord=getCompareWords(w1)
    rank_dict=[]
    for each in howNetWord:
        hybrid=wordsim(w1,each)
        if hybrid>score:
            rank_dict.append([each,hybrid])
    rank_dict=sorted(rank_dict,key=lambda item:item[1],reverse=True)
    ###去重
    words=[]
    rank_dict1=[]
    for each in rank_dict:
        if each[0] not in words:
            words.append(each[0])
            rank_dict1.append(each)
    return rank_dict1

### 获得HowNet中第n层的父节点
def getFathers(w1):
    global word2codeDict
    ### 暂时设定n=3
    n=3
    codes=word2codeDict[w1]
    print(codes)
    for i in range(3):
        fathers=[]
        for each in codes:
            ### 设置不能到达'-1'
            if code2fatherDict[each]==['-1']:
                fathers+=each
            else:
                fathers+=code2fatherDict[each]
        codes=fathers
    fathers=list(set(fathers))
    print(fathers)

### 获取与W1比较的词
def getCompareWords(w1):
    fathers=getFathers(w1)
    children=[]
    for each in fathers:
        children+=allHypo(each)
    words=[]
    for each in children:
        if str(each)>12251:
            words.append(code2wordDict[each])
    return words
#########################HowNet部分############################
#########################CiLin 部分############################
ci_lin = CilinSimilarity()
### open the Dict File ###
### 把字典录入进去，参数为文件名，返回值为一个列表[符号，具体词]
def openDictFile(filename):
    dictdata=[]
    ddf=open(filename)
    for line in ddf.readlines():
        data=line.split(" ")
        dictdata.append([data[0],data[1][0:-1]])
    ddf.close()
    return dictdata

### open the Raw Data File ###
### 把原始数据注入python，参数为文件名
def openRawDataFile(filename):
    rawdata=[]
    rdf=open(filename)
    for line in rdf.readlines():
        rawdata.append(line[0:-1])
    rdf.close()
    return rawdata

### Track the process, let people know the process ###
###查看进度，有一定的进度条条，参数为文件名
###写入数据到文件中
def processTrackInCilin(rawdata,filename):
    sim_dict = {}
    n=0
    for w1 in rawdata:
        result=open(filename,'a')
        rank_dict=CombineResult(w1)
        result.write("========================================\n")
        ### 写入这个单词
        result.write(w1.split(" ")[1]+":\n")
        ### 写入其相关词
        if rank_dict[0][1]==-1:
            result.write("{}\n")
        else:
            for each in rank_dict:
                result.write(str(each[0])+"\t"+str(each[1])+"\n")
        result.write("========================================\n")
        sim_dict[w1]=rank_dict
        n+=1
        ### 显示进度
        print("完成了"+str((n/len(rawdata))*100)+"%!")
        result.close()

### look up the word in the dictionary ###
### 利用字典法，找出相关度较高的词，参数为w1,code,dictionary和区段，输出为一个list
def findWord(w1,code,dictionary,dictrange):
    global score
    dictdata=dictionary
    rank_dict=[]
    code1=code
    code=code[0:dictrange]
    for dictlist in dictdata:
        if code in dictlist[0]:
            hybrid = ci_lin.sim2018(w1,dictlist[1])
            ###如果code的长度为8并且是“#”相关的关系，那么相关度需要再乘以0.85
            if code1[-1]=="#":
                hybrid*=0.85
            ###只有算出来大于score的才能加入清单
            ###并且需要去个重
            if (hybrid>score) :
                rank_dict.append([dictlist[1],hybrid,dictlist[0]])
    return rank_dict

### Combine the result from three dictionary ###
### 这个函数整合了三个词典里的数据，取得最大的数据段 ###
### 输入值为（单词，初始的位置）
### 这边这个方法是基于 [哈工大词林] 的
def CombineResult(w1):
    code,w1=w1.split(" ")
    ###exp Aa01A01= 人
    print('Start to combine words',code,w1)
    rank_dict=[]
    ###在第二层去匹配 (father)
    ###dict2->匹配第1位
    smalldict=openDictFile('smalldict-dict-2.txt')
    rank_dict=findWord(w1,code,smalldict,2)
    ###在第四层去匹配 (father)
    ###dict4->匹配前2位
    smalldict=openDictFile('smalldict-dict-4.txt')
    rank_dict+=findWord(w1,code,smalldict,4)
    ###在第五层去匹配（father）
    ###dict5->匹配前4位
    smalldict=openDictFile('smalldict-dict-5.txt')
    rank_dict+=findWord(w1,code,smalldict,5)
    ###在最底层去匹配（silibings）
    ###dict8->匹配前5位
    smalldict=openDictFile('smalldict-dict-8.txt')
    rank_dict+=findWord(w1,code,smalldict,5)
    ###将匹配的数据全部输出
    rank_dict=sorted(rank_dict,key=lambda item:item[1],reverse=True)
    ###去重
    words=[]
    rank_dict1=[]
    for each in rank_dict:
        if each[0] not in words:
            words.append(each[0])
            rank_dict1.append(each)

    return rank_dict1
#########################CiLin 部分############################
########################Combine部分#############################
def processTrackInCombine(rawdata,filename):
    sim_dict = {}
    n=0
    for w1 in rawdata:
        result=open(filename,'a')
        howNet_rank_dict=GetResult(w1.split(" ")[1])
        ciLin_rank_dict=CombineResult(w1)
        result.write("========================================\n")
        ### 写入这个单词
        result.write(w1.split(" ")[1]+":\n")
        ### 写入其相关词
        if len(howNet_rank_dict[0])==0 and ciLin_rank_dict[0][1]==-1:
            result.write("{}\n")
        else:
            rank_dict={}
            all_rank_dict=howNet_rank_dict+ciLin_rank_dict
            for each in all_rank_dict:
                if each[0] in rank_dict:
                    if each[1]>rank_dict[each[0]]:
                        rank_dict[each[0]]=each[1]
                else:
                    rank_dict[each[0]]=each[1]
            for each in rank_dict:
                result.write(str(each)+"\t"+str(rank_dict[each])+"\n")
        result.write("========================================\n")
        sim_dict[w1]=rank_dict
        n+=1
        ### 显示进度
        print("完成了"+str((n/len(rawdata))*100)+"%!")
        result.close()


########################### 词林的部分 #############################
rawdata=openRawDataFile('incilin.txt')
score=0.8
processTrackInCilin(rawdata,'cilinresult-0.8.txt')
score=0.85
processTrackInCilin(rawdata,'cilinresult-0.85.txt')
score=0.9
processTrackInCilin(rawdata,'cilinresult-0.9.txt')
########################### 知网的部分 #############################
A=openWordFile("A.txt")
score=0.8
processTrackInHowNet(A,"hownetresult-0.8.txt")
score=0.85
processTrackInHowNet(A,"hownetresult-0.85.txt")
score=0.9
processTrackInHowNet(A,"hownetresult-0.9.txt")
########################### 结合的部分 #############################
C=openWordFile("C-incilin.txt")
score=0.8
processTrackInCombine(C,"combineresult-0.8.txt")
score=0.85
processTrackInCombine(C,"combineresult-0.85.txt")
score=0.9
processTrackInCombine(C,"combineresult-0.9.txt")
