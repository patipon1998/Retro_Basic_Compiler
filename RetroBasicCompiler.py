import sys

grammar ={
    1 : ["line", "pgm"], #pgm -> line pgm
    2 : ["EOF"], #pgm -> EOF
    3 : ["lineNum", "stmt"], #line -> lineNum stmt
    4 : ["asgmnt"], #stmt -> asgmnt
    5 : ["if"], #stmt -> if
    6 : ["print"], #stmt -> print
    7 : ["goto"], #stmt -> goto
    8 : ["stop"], #stmt -> stop
    9 : ["id", "=", "exp"], #asgmnt -> id = exp
    10 : ["term", "exp'"], #exp -> term exp'
    11 : ["+", "term"], #exp' -> + term
    12 : ["-", "term"], #exp' -> - term
    13 : None, #exp' -> empty
    14 : ["id"], #term -> id
    15 : ["const"], #term -> const
    16 : ["IF", "cond", "lineNum"], #if -> IF cond lineNum
    17 : ["term", "cond'"], #cond -> term cond'
    18 : ["<", "term"], #cond' -> < term
    19 : ["=", "term"], #cond' -> = term
    20 : ["PRINT", "id"], #print -> PRINT id
    21 : ["GOTO", "lineNum"], #goto -> GOTO lineNum
    22 : ["STOP"] #stop -> STOP
}

parsing_table = {
    "pgm": {"lineNum": 1, "EOF": 2},
    "line": {"lineNum": 3},
    "stmt": {"id": 4, "IF": 5, "PRINT": 6, "GOTO": 7, "STOP": 8},
    "asgmnt": {"id": 9},
    "exp": {"id": 10, "const": 10},
    "exp'": {"+": 11, "-": 12,"EOF": 13, "lineNum": 13},
    "term": {"id": 14, "const": 15},
    "if": {"IF": 16},
    "cond": {"id": 17, "const": 17},
    "cond'": {"<": 18, "=": 19},
    "print": {"PRINT": 20},
    "goto": {"GOTO": 21},
    "stop": {"STOP": 22},
}

id = [chr(e) for e in range(ord('A'), ord('Z')+1)]
lineNum = [str(e) for e in range(1, 1001)]
const = [str(e) for e in range(0, 101)]
terminal = ["+", "-", "IF" ,"<","=", "PRINT", "GOTO", "STOP", "EOF"]
bCodeType = {
    "#line": 10,
    "#id": 11,
    "#const": 12,
    "#if": 13,
    "#goto": 14,
    "#print": 15,
    "#stop": 16,
    "#op": 17,
}

stack = ["EOF"]

def getTerminalType(token) :
    if token.isdigit():
        return "num"
    if token in terminal:
        return token
    if token in id:
        return "id"
    print("Invalid Input")
    exit()

def pairTerminal(token, top):
    termType = getTerminalType(token)
    if termType != "num":
        return termType == top
    else :
        return top == "lineNum" or top == "const"

def discipline(top,token):
    termType = getTerminalType(token)
    if termType != "num" and termType in parsing_table[top]:
        return parsing_table[top][termType]
    if "lineNum" in parsing_table[top]:
        return parsing_table[top]["lineNum"]
    if "const" in parsing_table[top]:
        return parsing_table[top]["const"]
    print("Invalid Grammar")
    exit()

def parser(token):
    while not pairTerminal(token, stack[-1]):
        top = stack.pop()
        if top not in parsing_table :
            print("Invalid Grammar555")
            exit()
        principle = discipline(top,token)
        if grammar[principle] != None :
            stack.extend(grammar[principle][::-1])
    if(stack[-1] == 'lineNum' and not 1 <= int(token) <= 1000):
        print("Invalid Grammar")
        exit()
    if(stack[-1] == 'const' and not 0 <= int(token) <= 100):
        print("Invalid Grammar")
        exit()
    return stack.pop()

def getBCode(term,val) :
    if(term == "+"):
        return ("#op", 1)
    if(term == "-"):
        return ("#op", 2)
    if(term == "<"):
        return ("#op", 3)
    if(term == "="):
        return ("#op", 4)
    if(term == "lineNum"):
        return ("#line", int(val))
    if(term == "id"):
        return ("#id", ord(val) - ord('A') + 1)
    if(term == "const"):
        return ("#const", int(val))
    if(term == "IF"):
        return ("#if", 0)
    if(term == "GOTO"):
        return ("#goto", int(val))
    if(term == "PRINT"):
        return ("#print", 0)
    if(term == "STOP"):
        return ("#stop", 0)

def genBCode(parsed) :
    bCodeList = list()
    for i in range(len(parsed)):
        if(parsed[i][0] not in ["GOTO","lineNum"] or i == 0):
            bCodeList.append(getBCode(parsed[i][0], parsed[i][1]))
        else:
            if(parsed[i][0] == 'lineNum' and i != 0):
                bCodeList.append(getBCode("GOTO",parsed[i][1]))
    return bCodeList

def toBCode(token):
    parsed = list()
    for tok in token :
        parsed.append((parser(tok),tok))
    bCodeList = genBCode(parsed)
    bCodeLine = ""
    for types, value in bCodeList:
        bCodeLine = bCodeLine + str(bCodeType[types]) + " " + str(value) + " "
    return bCodeLine.strip()
    
path = str(sys.argv[1])
fil = open(path,'r')
out = open('output.txt', 'w')
for count,line in enumerate(fil):
    if count == 0 :
        stack.append("pgm")
    tokens = line.strip().split()
    bcode = toBCode(tokens)
    print(bcode)
    out.write(bcode + "\n")
print("0")
out.write("0\n")
fil.close()
out.close()