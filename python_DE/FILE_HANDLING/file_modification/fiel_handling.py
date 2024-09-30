# #   FUNCTION TO GET COUNT OF LINES AND print specifcic line
def countofFile_specifcicLine(filename):
    with open(filename, 'r') as file:
        x = file.readlines()
        print(x)
        print(f"total lines in files:{len(x)}")

        if len(x) > 0:
            print(f"first line: {x[0].strip()}")

        if len(x) > 0:
            print(f"last line: {x[-1].strip()}")
# countofFile_specifcicLine("sample.txt")

# word frequency counter and get top 5
worddict = {}
chardict={}
def countt(e,type):
    if type =="word":
        if e[-1] == ".":
            e = e[0:len(e) - 1]
            if e =="":
                return None
        if e in worddict:
            worddict[e] += 1
        else:
            worddict[e]=1
    else:
        e=e.lower()
        if e =="." or e ==" " or e==",":
            return None
        if e in chardict:
            chardict[e]+=1
        else:
            chardict[e]=1
def word_frequency(filename,n,m):
    with open(filename, 'r') as file:
        x = file.readlines()
        result = "".join(map(str, x))

        for i in result:
            countt(str(i),"charr")

        unsorted_dict = dict(sorted(chardict.items(), key=lambda item: item[1], reverse=True))
        print(f"in char ,TOP {n}:")
        for i, (key, value) in enumerate(chardict.items()):
            if i < n:
                print("{{ {} : {} }}".format(key, value))
            else:
                break
        lst = result.split()
        for e in lst:
            countt(str(e),"word")
        unsorted_dict = dict(sorted(worddict.items(), key=lambda item: item[1], reverse=True))
        print(f"TOP {m}:")
        for i, (key, value) in enumerate(unsorted_dict.items()):
            if i < m:
                print("{{ {} : {} }}".format(key, value))
            else:
                break
# word_frequency("sample.txt",10,3)


#writing  in output file
def writing_to_Output_file(filenname):
    # Append vs write mode
    file1 = open(filenname, "w")
    i=1
    while i <100+1:
        file1.write(str(i))
        file1.write("\n")
        i+=1
    file1.close()
    file1 = open(filenname, "a")
    i=1
    while i < 11:
        file1.write(str(i**2))
        file1.write("\n")
        i += 1
# writing_to_Output_file("output.txt")

# renaming file content
def renaming_text_inFILE(filename,text,change,nfilename):
    with open(filename, 'r') as file:
        x = file.readlines()
        result = "".join(map(str, x))
        lst=result.split()
        s=""
        for i in lst:
            if i[0:3] ==text:
                i=change
                s+=i
                s+=" "
            else:
                s+=i
                s+=" "
        print(s)
        with open(nfilename,'w') as file:
            file.write(s)

renaming_text_inFILE("sample.txt", "Ear", "mars", "modified.txt")


#merging two fies
def merge_twoFILES(Ffilename,sfilename):
    with open(sfilename,'r') as sfile:
        s= sfile.read()
    with open(Ffilename,'a') as ffile:
        ffile.write(s)

merge_twoFILES("sample.txt","modified.txt")