import math
import sys
devfile  = open(sys.argv[1],encoding="utf8")
#devfile  = open("catalan_corpus_dev_raw.txt",encoding="utf8")
probfile = open("hmmmodel.txt")
#devTest = open("catalan_corpus_dev_tagged.txt", encoding="utf8")
tagMap = {}
wordMap = {}
lineList = []
count = 0
# Preparing Transition and Emission probabilities map
for i,line in enumerate(probfile):
    if i>0 and i<31:
        li = line.split('\t')
        transProb = {}
        j = 3
        while j < len(li)-1:
            transProb[li[j]] = math.log(float(li[j+1]))
            j += 2
        tagMap[li[0]] = [int(li[1]), int(li[2]), transProb]
    elif i>31:
        li = line.split('\t')
        wordProb = {}
        j = 1
        while j < len(li)-1:
            wordProb[li[j]] = math.log(float(li[j+1]))
            j += 2
        wordMap[li[0]] = wordProb

#Tagging of Development corpus
for line in devfile:
     sequenceMap = []
     word = line.split()
     #For first word
     firstWord = word[0]
     #firstWord = firstWord.lower()
     mapLength = len(tagMap)-1
     if firstWord in wordMap:
         transListFinal = []
         tranListFirst = {}
         tagList = wordMap[firstWord]
         for item in tagList.items():
             tranListFirst1 = {}
             if item[0] in tagMap["Q"][2]:
                 tranListFirst1[item[0]] = tagMap["Q"][2][item[0]] + item[1]
                 tranListFirst[item[0]] = tagMap["Q"][2][item[0]] + item[1]
             else:
                 tranListFirst1[item[0]] = math.log(1/(tagMap["Q"][1]+mapLength)) + item[1]
                 tranListFirst[item[0]] = math.log(1/(tagMap["Q"][1]+mapLength)) + item[1]
             transListFinal.append(["Q",tranListFirst1])
     else:
         transListFinal = []
         tranListFirst ={}
         for tag in tagMap.items():
             tranListFirst1 = {}
             if tag[0] != "Q":
                 if tag[0] in tagMap["Q"][2]:
                     tranListFirst1[tag[0]] = tagMap["Q"][2][tag[0]]
                     tranListFirst[tag[0]] = tagMap["Q"][2][tag[0]]
                 else:
                     tranListFirst1[tag[0]] = math.log(1/(tagMap["Q"][1]+mapLength))
                     tranListFirst[tag[0]] = math.log(1/(tagMap["Q"][1]+mapLength))
                 transListFinal.append(["Q", tranListFirst1])
     sequenceMap.append(transListFinal)
     # For words other than firsto
     for wd in word[1:]:
         #wd = wd.lower()
         if wd in wordMap:
             transListFinal = []
             tranListSecond = {}
             tagList = wordMap[wd]
             for item in tagList.items():
                 maxProb = -float("inf")
                 for transition in tranListFirst.items():
                     if item[0] in tagMap[transition[0]][2]:
                         prob = transition[1] + tagMap[transition[0]][2][item[0]] + item[1]
                     else:
                         prob = transition[1] + math.log(1/(tagMap[transition[0]][1]+mapLength)) + item[1]
                     if prob > maxProb:
                        maxProb = prob
                        initialTag = transition[0]
                 tranListSecond[item[0]] = maxProb
                 temMap = {}
                 temMap[item[0]] = tranListSecond[item[0]]
                 transListFinal.append([initialTag,temMap])
         else:
             transListFinal = []
             tranListSecond = {}
             for item in tagMap.items():
                 if item[0] != "Q":
                     maxProb = -float("inf")
                     for transition in tranListFirst.items():
                         if item[0] in tagMap[transition[0]][2] :
                             prob = transition[1] + tagMap[transition[0]][2][item[0]]
                         else:
                             prob = transition[1] + math.log(1 / (tagMap[transition[0]][1] + mapLength))
                         if prob > maxProb:
                             maxProb = prob
                             initialTag = transition[0]
                     tranListSecond[item[0]] = maxProb
                     temMap = {}
                     temMap[item[0]] = tranListSecond[item[0]]
                     transListFinal.append([initialTag, temMap])
         sequenceMap.append(transListFinal)
         tranListFirst = tranListSecond
     maxSeq = -float("inf")
     item = sequenceMap.pop(len(sequenceMap)-1)
     # word = line.split()
     length = len(word)-1
     finalSeq = []
     for it in item:
         for tag in it[1].items():
             if maxSeq < tag[1]:
                 maxSeq = tag[1]
                 maxTag = tag[0]
                 secLastTag = it[0]
     finalSeq.append(maxTag)
     for item in reversed(sequenceMap):
         for it in item:
             for tag in it[1].items():
                 if tag[0] == secLastTag:
                     finalSeq.append(tag[0])
                     newTag = it[0]
         secLastTag = newTag
     i=0
     word =line.split()
     line = []
     length = len(word)
     while i < len(word):
         line.append(word[i]+"/"+(finalSeq[len(word)-i-1]))
         i = i + 1
     lineList.append(line)
f = open("hmmoutput.txt", "w+")
for item in lineList:
    f.write(" ".join(item))
    f.write("\n")


# testList = []
# for line in devTest:
#     words =line.split()
#     testList.append(words)
# total = 0
# correct = 0
# for i, b in enumerate(testList):
#     for j, d in enumerate(b):
#         total += 1
#         if testList[i][j] == lineList[i][j]:
#             correct += 1
# print(correct)
# print("\n")
# print(total)
# print(correct*100/total)


# f = open("output1.txt" , "w+")
# f.write("TRANSITION PROBABILITIES" +"\n" )
# for line in tagMap.items():
#     f.write(line[0] + "\t" + "%d" % line[1][0] + "\t" + "%d" % line[1][1]+"\t")
#     for li in line[1][2].items():
#         f.write(li[0] + "\t" + "%f13" % li[1] + "\t")
#     f.write("\n")
# f.write("EMISSION PROBABILITIES" +"\n" )
# for line in wordMap.items():
#     f.write(line[0] + "\t")
#     for li in line[1].items():
#         f.write(li[0] + "\t" + "%f13" %li[1] + "\t")
#     f.write("\n")
