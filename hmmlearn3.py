import sys
textfile  = open(sys.argv[1],encoding="utf8")
#textfile  = open("catalan_corpus_train_tagged.txt",encoding="utf8")
tagMap = {}
wordMap = {}
for line in textfile:
    words = line.split()
    for i,word in enumerate(words):
        wordLen = len(word)
        onlyWord = word[0:wordLen-3]
        #onlyWord = onlyWord.lower()
        tag = word[-2:]
        if onlyWord not in wordMap:
            wordTag = {}
            wordTag.setdefault(tag,1)
            wordMap.setdefault(onlyWord,wordTag)
        else:
            if tag not in wordMap[onlyWord]:
                wordMap[onlyWord].setdefault(tag , 1)
            else:
                wordMap[onlyWord][tag] += 1
        if i == 0:
            if "Q" not in tagMap:
                transitionProbQ = {}
                transitionProbQ.setdefault(tag, 1)
                propertiesQ = [0, 1, transitionProbQ]
                tagMap.setdefault("Q", propertiesQ)
            else:
                if tag in tagMap["Q"][2]:
                    tagMap["Q"][2][tag] += 1
                else:
                    tagMap["Q"][2].setdefault(tag, 1)
                tagMap["Q"][1] += 1
        if tag not in tagMap:
            transitionProb = {}
            properties = [1,0]
            if i + 1 < len(words):
                properties[1] += 1
                nextTag = words[i + 1][-2:]
                transitionProb.setdefault(nextTag, 1)
            properties.append(transitionProb)
            tagMap.setdefault(tag, properties)
        else:
            tagMap[tag][0] += 1
            if i + 1 < len(words):
                tagMap[tag][1] += 1
                nextTag = words[i + 1][-2:]
                transprob = tagMap[tag][2]
                if nextTag not in transprob:
                     transprob.setdefault(nextTag, 1)
                else:
                     transprob[nextTag] += 1
for item in tagMap.items():
    for inItem in item[1][2].items():
        item[1][2][inItem[0]] = (inItem[1]+1) / (item[1][1] + (len(tagMap)-1))

for item in wordMap.items():
    for inItem in item[1].items():
        item[1][inItem[0]] = inItem[1] / tagMap[inItem[0]][0]
textfile.close()
f = open("hmmmodel.txt" , "w+")
f.write("TRANSITION PROBABILITIES" +"\n" )
for line in tagMap.items():
    f.write(line[0] + "\t" + "%d" % line[1][0] + "\t" + "%d" % line[1][1]+"\t")
    for li in line[1][2].items():
        f.write(li[0] + "\t" + "%f13" % li[1] + "\t")
    f.write("\n")
f.write("EMISSION PROBABILITIES" +"\n" )
for line in wordMap.items():
    f.write(line[0] + "\t")
    for li in line[1].items():
        f.write(li[0] + "\t" + "%f13" % li[1] + "\t")
    f.write("\n")