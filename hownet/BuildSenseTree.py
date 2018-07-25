### 整理【义原+抽象概念+义项】树的处理流
### 用法，根据1.2.3...的编号依次打开注释然后关闭注释

### 1.载入义原
# f=open("WHOLE.DAT")
# datas=[]
# for line in f.readlines():
#     data=line.split()
#     datas.append(data[1])
# f.close()



### 2.提取所有的【概念】&【概念+名字】
# f2=open("glossary.txt")
# abstract_concepts=[]
# for line in f2.readlines():
#     data=line.split("/")
#     senses=data[2].split(",")
#     abstract_concept=""
#     for each in senses:
#         if each[0].isalpha():
#             ### 有等号的时候
#             if "=" in each:
#                 abstract_concept+="∩"+each
#             else:
#                 abstract_concept+="\t"+each
#         ### 是虚概念的时候
#         elif each[0]=="{":
#             abstract_concept+="\t"+each
#         else:
#             abstract_concept+="∩"+each
#     abstract_concept=abstract_concept[1:-1]
# #     abstract_concepts.append(data[0]+":"+abstract_concept+"\n")
# # f3=open("all_concepts+name.txt","w")
#     abstract_concepts.append(abstract_concept+"\n")
# f3=open("all_concepts.txt","w")
# f3.writelines(abstract_concepts)
# f3.close
# f2.close()



### 3.提取所有抽象概念
### tips:这一步需要把 "1" 也打开
# f2=open("all_concepts.txt")
# abstract_concepts=[]
# for line in f2.readlines():
#     ### 如果是虚概念，那么把拆开
#     if "{" in line:
#         line=line.strip()[1:-1]
#
#     data=line.split("\t")
#     for each in data:
#         abstract_concept=each.strip()
#         if abstract_concept not in datas:
#             if (abstract_concept+"\n") not in abstract_concepts:
#                 abstract_concepts.append(abstract_concept+"\n")
#
# f3=open("abstract_concepts.txt","w")
# f3.writelines(abstract_concepts)
# f3.close
# f2.close()



### 4.整理抽象概念和实概念在一个词典里
### 4.1 整理实概念
# f=open("WHOLE.DAT")
# concepts=[]
# for line in f.readlines():
#     data=line.split()
#     concept=""
#     for each in data:
#         concept+=each+"\t"
#     concepts.append(concept[:-1]+"\n")
# print(concepts)
# f2=open("HowNetDict.txt","w")
# f2.writelines(concepts)
# f2.close()
# f.close()

### 4.2 整理抽象概念
### （ps:我要吐槽，这个地方，这个垃圾HowNet里还有很多没弄好的地方
###  (所以需要很努力的嗯。。。手工整理了一下午呵呵哒
# f=open("WHOLE.DAT")
# ### 出现了一次的义原
# datas={}
# ### 出现了两次的义原
# datas_double={}
# ### 出现了三次的义原
# datas_triple={}
# for line in f.readlines():
#     data=line.split()
#     if data[1] not in datas:
#         datas[data[1]]=data[0]
#     elif data[1] not in datas_double:
#         datas_double[data[1]]=data[0]
#     else:
#         datas_triple[data[1]]=data[0]
# f.close()
# n=1622
# f1=open("abstract_concepts.txt")
# concepts=[]
# vague_concepts=[]
# for line in f1.readlines():
#     concept=[]
#     father=-1
#     data=line.split("∩")
#     if data[0].strip() in datas:
#         father=datas[data[0].strip()]
#     elif (data[0][0]=="^") or (data[0][0]=="*") or (data[0][0]=="#"):
#         if data[0][1:].strip() in datas:
#             father=datas[data[0][1:].strip()]
#     else:
#         print(data)
#     if father!=-1:
#         concepts.append(str(n)+"\t"+line[:-1]+"\t"+str(father)+"\n")
#     else:
#         vague_concepts.append(str(n)+"\t"+line[:-1]+"\t"+str(father)+"\n")
#     n+=1
# f1.close()
# ### 保存正确的数据
# f2=open("AbstractConceptDict.txt","w")
# f2.writelines(concepts)
# ### 保存出错数据，并且利用手工更改其
# f2=open("VagueAbstractConceptDict.txt","w")
# f2.writelines(vague_concepts)
# f2.close()

### 4.3 整理抽象概念2
# ### 抽象概念接抽象概念
# f=open("AbstractConceptDict.txt")
# ###它原本的位置的字典
# AbstractConceptDict={}
# ###它父结点的字典
# AbstractConceptFatherDict={}
# ###根据长度的字典
# all_lens={}
# ###把三个字典填满
# for line in f.readlines():
#     data=line[:-1].split("\t")
#     AbstractConceptDict[data[1]]=data[0]
#     AbstractConceptFatherDict[data[1]]=data[2]
#     lens=len(data[1].split("∩"))
#     if lens in all_lens:
#         all_lens[lens].append(data[1])
#     else:
#         all_lens[lens]=[data[1]]
# ###数一数字典有多长 哦，数出来是1-7,那么从2开始挂树
# for i in range(2,8):
#     for each in all_lens[i]:
#         for each1 in all_lens[i-1]:
#             if each1 in each and (each.index(each1))==0:
#                     AbstractConceptFatherDict[each]=AbstractConceptDict[each1]
#
# NewAbstractConcepts=[]
# for each in AbstractConceptFatherDict:
#     line=str(AbstractConceptDict[each])+"\t"+each+"\t"+str(AbstractConceptFatherDict[each])+"\n"
#     NewAbstractConcepts.append(line)
#
# f1=open("AbstractConceptDict2.txt","w")
# f1.writelines(NewAbstractConcepts)
# f1.close()
# f.close()

### 4.4整理义项与抽象概念的关系
### 打开所有抽象概念
# f2=open("AbstractConceptDict2.txt")
# ###它原本的位置的字典
# AbstractConceptDict={}
# for line in f2.readlines():
#     data=line[:-1].split("\t")
#     AbstractConceptDict[data[1]]=data[0]
# f2.close()
# ### 打开义原概念
# f3=open("HowNetDict.txt")
# ###它原本的位置的字典
# RealConceptDict={}
# for line in f3.readlines():
#     data=line[:-1].split("\t")
#     RealConceptDict[data[1]]=data[0]
# ### 打开所有概念,为它们找父结点
# f1=open("all_concepts+name.txt")
# all_words=[]
# n=12251
# for line in f1.readlines():
#     word=[]
#     fathers=""
#     data=line.split(":")
#     if data[1][0]=="{":
#         senses=data[1][1:-2]
#     else:
#         senses=data[1][:-1]
#     concepts=senses.split("\t")
#     for concept in concepts:
#         concept=concept.strip()
#         if len(concept)>0:
#             if concept in AbstractConceptDict:
#                 fathers+=str(AbstractConceptDict[concept])+","
#             else:
#                 fathers+=str(RealConceptDict[concept])+","
#     word=str(n)+"\t"+data[0]+"\t"+fathers[:-1]+"\n"
#     all_words.append(word)
#     n+=1
# f1.close()
# f4=open("AllConceptDict.txt","w")
# f4.writelines(all_words)
# f4.close()

### 5.给整个SenseTree加一个根节点 0 null|空 -1
# f=open("SenseTree.txt")
# concepts=[]
# for line in f.readlines():
#     data=line[:-1].split("\t")
#     code=str(int(data[0])+1)
#     word=data[1]
#     father=data[2].split(",")
#     fathers=""
#     for each in father:
#         each=str(int(each)+1)
#         fathers+=each+","
#     fathers=fathers[:-1]
#     concept=""
#     if code==fathers:
#         fathers='0'
#     concept=code+"\t"+word+"\t"+fathers+"\n"
#     concepts.append(concept)
# f1=open("NewSenseTree.txt","w")
# f1.writelines(concepts)
# f1.close()
# f.close()
