import math

###########################一些函数们######################################
### 利用Lin的方法计算相似度
### 这里的C1，C2都是code
def codesim(C1,C2):
    ###### 这里把2改为2.6可以使得结果更为相近
    sim=(2.6*ic(lsc(C1,C2),'-1'))/(ic(C1,lsc(C1,C2))+ic(C2,lsc(C1,C2)))
    return sim

### 利用Zhu的方法计算信息含量x
### 这里的c是指code
def ic(c1,c2):
    ### 包括根节点的所有节点
    max_nodes=78435
    ### 根节点到最低点的深度为17
    max_depth=17
    ### 按照论文里说的k取0.8 又按照实际修改成0.6
    k=0.6
    left=k*(1-(math.log(abs(hypo(c1))+1)/math.log(max_nodes)))
    right=(1-k)*(depth(c1,c2)/max_depth)
    return (left+right)

### 打开词典
### 返回值是包含三个字典的List
def openDictFile(filename):
    ###word2codeDict格式: {词:[code1，code2...]}
    ###并且这个是从n>12251才开始计算的
    word2codeDict={}
    ###code2fatherDict格式: {code:[father1,father2...]}
    code2fatherDict={}
    ###father2codeDict格式: {father:[code1,code2...]}
    father2codeDict={}
    ###code2wordDict格式: {code:word}
    code2wordDict={}
    f=open(filename+".txt")
    for line in f.readlines():
        data=line[:-1].split("\t")
        code=data[0]
        word=data[1]
        fathers=data[2].split(",")
        ###填充code2fatherDict的字典
        code2fatherDict[code]=fathers
        ###填充code2wordDict的字典
        code2wordDict[code]=word
        ###填充father2codeDict的字典
        for each in fathers:
            if each not in father2codeDict:
                father2codeDict[each]=[code]
            else:
                father2codeDict[each].append(code)
        ###填充word2codeDict的字典
        if int(code)>12251:
            if word not in word2codeDict:
                word2codeDict[word]=[code]
            else:
                word2codeDict[word].append(code)
    f.close()
    return [word2codeDict,code2fatherDict,father2codeDict,code2wordDict]

### 计算下面节点数的函数
### 获取所有的节点数
def allHypo(c):
    global father2codeDict
    nodes=[]
    if c in father2codeDict:
        nodes+=father2codeDict[c]
        for each in father2codeDict[c]:
            if each in father2codeDict:
                nodes+=allHypo(each)
    return nodes

### 计算所有节点数
def hypo(c):
    nodes=list(set(allHypo(c)))
    return len(nodes)

### 获取所有从c点到根节点的所有的路径
def getRoutines(c):
    global code2fatherDict
    routines=[]
    routine=[]
    def getDeeper(c):
        global code2fatherDict
        nonlocal routines
        nonlocal routine
        depth=0
        if c=='-1':
            routines.append(routine)
            routine=[]
        else:
            for each in code2fatherDict[c]:
                routine.append(each)
                getDeeper(each)
    getDeeper(c)
    return routines

#获取某个节点到根节点的最短距离
def getShortestPathLens(c):
    routines=getRoutines(c)
    if len(routines)==0:
        return -1
    #### 用某一个不可能达到的值作为原始的起点 233333
    len_=500000000
    for each in routines:
        len_=min(len_,len(each)-1)
    return len_

### 计算c1和c2的根节点
def lsc(c1,c2):
    lcsCodes=[]
    routines1=getRoutines(c1)
    routines2=getRoutines(c2)
    for routine1 in routines1:
        for routine2 in routines2:
            for each in routine1:
                if each in routine2:
                    lcsCodes.append(each)
    lcsCodes=list(set(lcsCodes))
    lcscode="-1"
    path=0
    for each in lcsCodes:
        if each is not '-1':
            if path<max(path,getShortestPathLens(each)):
                path=max(path,getShortestPathLens(each))
                lcscode=each
    return lcscode

### 获取它的深度
def depth(c1,c2):
    if c1=="-1":
        return 0
    rightroutines=[]
    routines=getRoutines(c1)
    for each in routines:
        if c2 in each:
            rightroutines.append(each)
    len_=500000000
    for each in rightroutines:
        len_=min(len(each),len_)
    return len_

### 获取词的code
def wordsim(w1,w2):
    global word2codeDict
    codes1=word2codeDict[w1]
    codes2=word2codeDict[w2]
    sim=0
    for code1 in codes1:
        for code2 in codes2:
            sim=max(sim,codesim(code1,code2))
    return sim


############################     启动字典    #########################
list_dict=openDictFile("./hownet/NewSenseTree")
word2codeDict=list_dict[0]
code2fatherDict=list_dict[1]
father2codeDict=list_dict[2]
code2wordDict=list_dict[3]
