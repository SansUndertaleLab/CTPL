characters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
numbers="1234567890"
special=":= ;+-*/"
class Endcode(Exception):
    pass
def throwError(errortype, msg, line):
    print(errortype+" on line "+str(line)+":\n\t"+msg)
    raise Endcode
def isAN(val):
    try:
        int(val)
    except ValueError:
        return False
    else:
        return True
def qualify(name):
    return not name=="" and not name=="\n" and not name=="\t"
def evaluatetype(char):
    global characters
    global numbers
    global special
    if char in characters:
        return "character"
    elif char in numbers:
        return "numbers"
    elif char in special:
        return "special"
with open("test.ctpl","r") as file:
    boxes=[]
    name=""
    ptype=""
    read=file.read().split(";")
    index=0
    for i in read:
        if i=="":
            read.pop(index)
        index+=1
    for i in read:
        tokens=[]
        iterator=0
        for j in i:
            if iterator==0:
                ptype=evaluatetype(i[0])
            iterator+=1
            ctype=evaluatetype(j)
            if not ptype==ctype:
                if not (ptype=="character" and ctype=="numbers"):
                    ptype=ctype
                    name=name.replace(" ","")
                    if qualify(name):
                        tokens.append(name)
                    name=""
            name+=j
        name=name.replace(" ","")
        if qualify(name):
            tokens.append(name)
            name=""
        boxes.append(tokens)
stack=[]
env={}
line=0
try:
    for i in boxes:
        line+=1
        action="NONE"
        payload=[]
        setvalue=""
        location=""
        for j in i[::-1]:
            #evaluate
            if action=="NONE":
                pass
            elif action=="SET":
                location=j
                setvalue=stack.pop(0)
                action="GETTYPE"
            elif action=="GETTYPE":
                validtypes=["int"]
                if not j in validtypes:
                    throwError("TypeError", "Unknown type: \""+j+"\"",line)
                if j=="int":
                    setvalue=int(setvalue)
                env[location]=setvalue
            if isAN(j):
                stack.append(j)
                action="NONE"
            else:
                if j==":=":
                    action="SET"
    print(env)
except Endcode:
    pass
