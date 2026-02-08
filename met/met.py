import sys
import string
import copy
import os
#DIMITRIOS NIKOLAOS KIFOKERIS AM:4083
#EVAGGELOS SAPOUNTZIS AM:4280
#den doulevei o ipologismos tou offset,frameLength,startingQuad kai episis den tiponei arxeio symb.
#sto prohgoumeno turn in h print_symbol_table diavaze tis metavlites alla den tipone swsta to onoma,twra diavazei swsta ta onomata twn metavlitwn
#gia kapion logo otan kaloume thn final() sthn block grafei to programa assembly se arxeio asm alla den doulevei swsta o pinakas simvolwn kai to cfile arxeio, gi afto tn valame se sxoleia
numbers=['0','1','2','3','4','5','6','7','8','9']
alphabet =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']                    
file= open(sys.argv[1], 'r')


#chars gia ton transition_matrix
white_character=0
num=1
letters=2
plus=3
minus=4
multiply=5
divide=6
greater_than=7
less_than=8
equal=9
l_parenthesis=10
r_parenthesis=11
l_bracket=12
r_bracket=13
l_block=14
r_block=15
end_of_file=16
full_stop=17
comma=18
hashtag=19
questionmark=20
collon=21
change_l=22
not_acceptable_sym=23

#conditions
cond_start=0
cond_letter=1
cond_num=2
cond_greater_than=3
cond_less_than=4
cond_assignment=5#condition gia tn anathesi
cond_comment=6

#tokens
id_tk=300
num_tk=301
plus_tk=302
minus_tk=303
multiply_tk=304
divide_tk=305
greater_than_tk=306
less_than_tk=307
equal_tk=308
l_parenthesis_tk=309
r_parenthesis_tk=310
l_bracket_tk=311
r_bracket_tk=312
l_block_tk=313
r_block_tk=314
end_of_file_tk=315
full_stop_tk=316
comma_tk=317
questionmark_tk=318
assignment_tk=319 #token gia anathesh
diff_tk=320
greater_or_equal_tk=321
less_or_equal_tk=322


binding_words=['print','if','else','while','program' ,'declare','case','switchcase','forcase','incase','default','and','or','not',
                                        'function','procedure','call','return','input','in','inout']
                                        
print_tk=100  
if_tk=101
else_tk=102
while_tk=103                       
program_tk=104
declare_tk=105
case_tk=106
switchcase_tk=107
forcase_tk=108
incase_tk=109
default_tk=110
and_tk=111
or_tk=112
not_tk=113
function_tk=114
procedure_tk=115
call_tk=116
return_tk=117
input_tk=118
in_tk=119
in_out_tk=120

#errors
error_not_acceptable_sym=401
error_digit_letter=402
error_more_than_30_chars=403
error_collon=404
error_num_out_of_bound=405
error_open_commments_with_eof=406



transition_matrix=[
          #condition start 
           [cond_start,cond_num,cond_letter,plus_tk,minus_tk,multiply_tk, divide_tk,
     cond_greater_than,cond_less_than,equal_tk,l_parenthesis_tk,r_parenthesis_tk,l_bracket_tk,r_bracket_tk,l_block_tk,r_block_tk,
         end_of_file_tk,full_stop_tk,comma_tk,cond_comment,questionmark_tk,cond_assignment,
         cond_start,error_not_acceptable_sym],
        
		#cond_letter
        [id_tk,cond_letter,cond_letter,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,
         id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,id_tk,error_not_acceptable_sym],
		 
		#condition num		 
        [num_tk,cond_num,error_digit_letter,num_tk,num_tk,num_tk,
         num_tk,num_tk,num_tk,num_tk,num_tk,
         num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,num_tk,
         num_tk,num_tk,num_tk,num_tk,error_not_acceptable_sym],

		#condition greater than
        [greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk,
         greater_than_tk,greater_or_equal_tk,greater_than_tk,greater_than_tk,greater_than_tk,error_not_acceptable_sym,
         greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk,
         greater_than_tk,greater_than_tk,greater_than_tk,greater_than_tk],

		#condition less than
        [less_than_tk,less_than_tk,less_than_tk,less_than_tk,less_than_tk,less_than_tk,
         less_than_tk,less_or_equal_tk,less_than_tk,diff_tk,less_than_tk,
         less_than_tk,less_than_tk,less_than_tk,less_than_tk,less_than_tk,less_than_tk,less_than_tk,less_than_tk,
         less_than_tk,less_than_tk,less_than_tk,less_than_tk,error_not_acceptable_sym],
        
        #condition assignment
        [error_collon,error_collon,error_collon,error_collon,error_collon,error_collon,
         error_collon,error_collon,error_collon,assignment_tk,error_collon,
         error_collon,error_collon,error_collon,error_collon,error_collon,error_collon,error_collon,error_collon,
         error_collon,error_collon,error_collon,error_collon,error_not_acceptable_sym],

        #condition comment
        [cond_comment,cond_comment,cond_comment,cond_comment,cond_comment,cond_comment,
         cond_comment,cond_comment,cond_comment,cond_comment,cond_comment,
         cond_comment,cond_comment,cond_comment,cond_comment,cond_comment,error_open_commments_with_eof,cond_comment,cond_comment,cond_start,cond_comment,
         cond_comment,cond_comment,cond_comment,cond_start]
        ]
l=1
def lex():
        global l
        cur= cond_start 
        word=''             
        lcount= l
        lex_result=[]
        while(cur>=0 and cur<=6):
                char = file.read(1)

                if (char == ' ' or char == '\t'):
                        char_tk = white_character
                elif (char in numbers):
                        char_tk = num

                elif (char in alphabet):
                        char_tk = letters

                elif (char == '+'):
                        char_tk = plus
                elif (char == '-'):
                        char_tk = minus
                elif (char == '*'):
                        char_tk = multiply
                elif (char == '/'):
                        char_tk = divide
                elif (char == '>'):
                        char_tk = greater_than
                elif (char == '<'):
                        char_tk = less_than    
                elif(char == '='):
                        char_tk = equal
                elif (char == '('):
                        char_tk = l_parenthesis
                elif (char == ')'):
                        char_tk = r_parenthesis
                elif (char == '['):
                        char_tk = l_bracket
                elif (char == ']'):
                        char_tk = r_bracket
                elif (char == '{'):
                        char_tk = l_block
                elif (char == '}'):
                        char_tk = r_block
                elif (char == ''):  
                        char_tk = end_of_file
                elif (char == '.'):
                        char_tk = full_stop
                elif (char == ','):
                        char_tk = comma
                elif (char == '#'):
                        char_tk = hashtag
                elif (char == ';'):
                        char_tk = questionmark
                elif (char == ':'):
                        char_tk = collon
                elif (char == '\n'):
                        lcount=lcount+1
                        char_tk = change_l
                else:
                        char_tk = not_acceptable_sym
    
                cur=transition_matrix[cur][char_tk]
                
                if(len(word)<30):
                        if(cur!=cond_start and cur!=cond_comment):
                                        word+=char
                else:
                        cur=error_more_than_30_chars

        if(cur==id_tk or cur==num_tk or cur==less_than_tk or cur==greater_than_tk ):
                if (char == '\n'):
                        lcount -= 1
                char=file.seek(file.tell()-1,0)  
                word = word[:-1]        

        if(cur==id_tk):
                if(word in binding_words):
                        if (word == 'print'):
                                cur = print_tk
                        elif (word == 'if'):
                                cur = if_tk
                        elif (word == 'else'):
                                cur = else_tk
                        elif (word == 'while'):
                                cur = while_tk
                        elif(word=='program'):
                                cur=program_tk
                        elif(word=='declare'):
                                cur=declare_tk
                        elif (word == 'case'):
                                cur = case_tk
                        elif (word == 'switchcase'):
                                cur = switchcase_tk
                        elif (word == 'forcase'):
                                cur = forcase_tk
                        elif (word == 'incase'):
                                cur = incase_tk    
                        elif (word == 'default'):
                                cur = default_tk
                        elif (word == 'and'):
                                cur = and_tk
                        elif (word == 'or'):
                                cur = or_tk
                        elif (word == 'not'):
                                cur = not_tk
                        elif (word == 'function'):
                                cur = function_tk
                        elif (word == 'procedure'):
                                cur = procedure_tk
                        elif (word == 'call'):
                                cur = call_tk
                        elif (word == 'return'):
                                cur = return_tk
                        elif (word == 'input'):
                                cur = input_tk
                        elif (word == 'in'):
                                cur = in_tk
                        elif (word == 'inout'):
                                cur = in_out_tk

        if (cur == num_tk):
                if (word.isdigit() >= pow(2,32)):
                    cur = error_num_out_of_bound

        if(cur==error_not_acceptable_sym):
                print("error: not acceptable symbol")
        elif(cur==error_digit_letter):
                print("error: there is letter after digit")
        elif(cur==error_more_than_30_chars):
                print("error: this word has more than 30 characters")
        elif(cur==error_collon):
                print("error: there is  a collon without the equal symbol next to it")
        elif(cur==error_num_out_of_bound):
                print("error: the number is not in this space [-(2^32-1),2^32-1]")
        elif(cur==error_open_commments_with_eof):
                print("error: the comment was not closed properly")

        lex_result.append(cur)
        lex_result.append(word) 
        lex_result.append(lcount)
        l=lcount
        #print (lex_result)
        return lex_result

# endiamesos kwdikas
global listofQuads
listofQuads = []
tempvariablelist = []
countQuad = 1
T_i = 1


def nextQuad():#epistrefei ton ari8mo ths epomenhs tetradas 
    global countQuad
    return countQuad

def genQuad(first, second, third, fourth):#ftiaxnei thn epomenh tetrada
    global countQuad
    global listofQuads
    list = []
    list = [nextQuad()]
    list += [first] + [second] + [third] + [fourth]
    countQuad +=1
    listofQuads += [list]
    return list


def newTemp():#ftiaxnei kai epistrefei metavlith  T_1,2,3..
    global T_i
    global tempvariablelist
    list = ['T_']
    list.append(str(T_i))
    tempvariable="".join(list)
    T_i +=1
    tempvariablelist += [tempvariable]

    entity = Entity()
    entity.name = tempvariable
    entity.type = 'TEMP'
    new_entity(entity)
    return tempvariable

def makeList(x):#ftiaxnei mia lista etiketwn tetradwn pou apoteliste mono to x
    thisList = [x]
    return thisList


def emptyList():#ftiaxnei mia kenh lista tetradwn
    pointerList = []
    return pointerList


def mergeList(list1, list2):#apo tn sinenwsh 2 listwn (list1 kai list2) ftiaxnei mia lista etiketwn  tetradwn
    list=[]
    list += list1 + list2

    return list


def backPatch(list, z):#to list apotelite apo deiktes  se tetrades stis opies to telefteo stoixeio einai keno, h backpatch episkeptete aftes tis tetrades kai tis simplirwne me tn epiketa z
    global listofQuads
    for i in range(len(list)):
        for j in range(len(listofQuads)):
            if(list[i]==listofQuads[j][0]):
                listofQuads[j][4] = z
                break;
    return
#pinakas simvolwn
topScope = None
class Scope():#kiklos
        def __init__(self):
                self.name = ''
                self.entityList = []
                self.nestingLevel = 0
                self.surroundingScope = None


class Argument():#orthogonio
        def __init__(self):
                self.name = ''
                self.type = 'INT'
                self.parameterMode = ''


class Entity():#trigono

        def __init__(self):
                self.name = ''
                self.type = ''
                self.parameter = self.Parameter()
                self.variable = self.Variable()
                self.tempvar = self.TemporaryVariable()
                self.subprogram = self.SubProgram()

        class Parameter: 
                def __init__(self):
                        self.mode = ''
                        self.offset = 0

        class Variable: 
                def __init__(self):
                        self.type = 'INT'
                        self.offset = 0

        class TemporaryVariable: 
                def __init__(self):
                        self.offset = 0

        class SubProgram: 
                def __init__(self):
                        self.type = ''
                        self.startingQuad = 0
                        self.frameLength = 0
                        self.argumentList = []


                        

def new_argument(object): 
        global topScope
        topScope.entityList[-1].subprogram.argumentList.append(object) 
        
def new_entity(object):  
        global topScope
        topScope.entityList.append(object)  


def delete_scope(): 
        global topScope
        nullScope = topScope
        topScope = topScope.surroundingScope 
        del nullScope

def add_parameters(): 
        global topScope
        
        for arg in topScope.surroundingScope.entityList[-1].subprogram.argumentList: 
                entity = Entity()
                entity.name = arg.name
                entity.type = 'PARAMETER'
                entity.parameter.mode = arg.parameterMode
                new_entity(entity)

def new_scope(name):  
        global topScope

        nextScope = Scope()
        nextScope.surroundingScope=topScope    
        nextScope.name = name
        if(topScope == None): 
                nextScope.nestingLevel = 0
        else:
                nextScope.nestingLevel = topScope.nestingLevel + 1
        topScope = nextScope
        


def print_symbol_table():
        global topScope

        tscope=topScope
        while tscope != None:
                print("SCOPE: "+"name:"+tscope.name+" nestingLevel:"+str(tscope.nestingLevel))
                print("\tENTITIES:")
                for entity in tscope.entityList:
                        if(entity.type == 'TEMP'):
                                print("\tENTITY: "+" name:"+str(entity.name)+"\t type:"+str(entity.type)+"\t temp type:"+str(entity.variable.type)+"\t offset:"+str(entity.tempvar.offset))
                        elif(entity.type == 'VAR'):
                                print("\tENTITY: "+" name:"+str(entity.name)+"\t type:"+str(entity.type)+"\t variable type:"+str(entity.variable.type)+"\t offset:"+str(entity.variable.offset))
                        elif(entity.type == 'PARAMETER'):
                                print("\tENTITY: "+" name:"+str(entity.name)+"\t type:"+str(entity.type)+"\t mode:"+str(entity.parameter.mode)+"\t offset:"+str(entity.parameter.offset))
                        elif(entity.type == 'SUBPROGRAM'):
                                if(entity.subprogram.type == 'Function'):
                                        print("\tENTITY: "+" name:"+str(entity.name)+"\t type:"+str(entity.type)+"\t function type:"+str(entity.subprogram.type)+"\t frameLength:"+str(entity.subprogram.frameLength)+"\t startingQuad:"+str(entity.subprogram.startingQuad))
                                        print("\t\tARGUMENTS:")
                                        for arg in entity.subprogram.argumentList:
                                                print("\t\tARGUMENT: "+" name:"+str(arg.name)+"\t type:"+str(arg.type)+"\t parameterMode:"+str(arg.parameterMode))
                                elif(entity.subprogram.type == 'Procedure'):
                                        print("\tENTITY: "+" name:"+str(entity.name)+"\t type:"+str(entity.type)+"\t procedure type:"+str(entity.subprogram.type)+"\t frameLength:"+str(entity.subprogram.frameLength)+"\t startingQuad:"+str(entity.subprogram.startingQuad))
                                        print("\t\tARGUMENTS:")
                                        for arg in entity.subprogram.argumentList:
                                                print("\t\tARGUMENT: "+" name:"+str(arg.name)+"\t type:"+str(arg.type)+"\t parameterMode:"+str(arg.parameterMode))
                tscope = tscope.surroundingScope

#telikos kwdikas
File = open('File.asm','w')
File.write('         \n\n\n') 

def search_Symtable(n):
    global topScope
    tscope = topScope
    while tscope != None:
        for entity in tscope.entityList:
            if(entity.name == n):
                return (tscope,entity)
        tscope=tscope.surroundingScope
    exit()

def loadvr(v,r): 
    global File
    global topScope

    if v.isdigit():
        File.write('li t%d,%s\n' % (r,v))
    else: 
        (scop,ent)=search_Symtable(v)

        if scop.nestingLevel==0 and ent.type=='VAR':
                File.write('lw t%d,-%d(gp)\n' % (r,ent.variable.offset))

        elif scop.nestingLevel==0 and ent.type=='TEMP': 
                File.write('lw t%d,-%d(gp)\n' % (r,ent.tempvar.offset))

        elif scop.nestingLevel == topScope.nestingLevel: 
            if ent.type=='VAR': 
                    File.write('lw t%d,-%d(sp)\n' % (r,ent.variable.offset))

            elif ent.type=='TEMP': 
                    File.write('lw t%d,-%d(sp)\n' % (r,ent.tempvar.offset))

            elif ent.type=='PARAMETER' and ent.parameter.mode=='CV': 
                    File.write('lw t%d,-%d(sp)\n' % (r,ent.parameter.offset))

            elif ent.type=='PARAMETER' and ent.parameter.mode=='REF': 
                    File.write('lw t0,-%d(sp)\n' % (ent.parameter.offset))
                    File.write('lw t%d,(t0)\n' % (r))

        #elif scop.nestingLevel < topScope.nestingLevel: 
            #if ent.type=='VAR':
                    #gnlvcode(v)
                    #File.write('lw t%d,(t0)\n' % (r))

            #elif ent.type=='PARAMETER' and ent.parameter.mode=='CV':
                    #gnlvcode(v)
                    #File.write('lw t%d,(t0)\n' % (r))

            #elif ent.type=='PARAMETER' and ent.parameter.mode=='REF':
                    #gnlvcode(v)
                    #File.write('lw t0,(t0)\n')
                    #File.write('lw t%d,(t0)\n' % (r))

def storerv(r,v): 
    global File
    global topScope

    (scop,ent) = search_Symtable(v)

    if scop.nestingLevel==0 and ent.type=='VAR':
        File.write('sw t%d,-%d(gp)\n' % (r,ent.variable.offset))
    elif scop.nestingLevel==0 and ent.type=='TEMP':
        File.write('sw t%d,-%d(gp)\n' % (r,ent.tempvar.offset))
    elif scop.nestingLevel == topScope.nestingLevel:
        if ent.type=='VAR':
            File.write('sw t%d,-%d(sp)\n' % (r,ent.variable.offset))

        elif ent.type=='TEMP':
            File.write('sw t%d,-%d(sp)\n' % (r,ent.tempvar.offset))

        elif ent.type=='PARAMETER' and ent.parameter.mode=='CV':
            File.write('sw t%d,-%d(sp)\n' % (r,ent.parameter.offset))

        elif ent.type=='PARAMETER' and ent.parameter.mode=='REF':
            File.write('lw t0,-%d(sp)\n' %  (ent.parameter.offset))
            File.write('sw t%d,(t0)\n' % (r))

    #elif scop.nestingLevel < topScope.nestingLevel:
        #if ent.type=='VAR':
            #gnlvcode(v)
            #File.write('sw t%d,(t0)\n' % (r))
        #elif ent.type=='PARAMETER' and ent.parameter.mode=='CV':
            #gnlvcode(v)
            #File.write('sw t%d,(t0)\n' % (r))

        #elif ent.type=='PARAMETER' and ent.parameter.mode=='REF':
            #gnlvcode(v)
            #File.write('lw t0,(t0)\n')
            #File.write('sw t%d,(t0)\n' % (r))



def final(): 
    global File
    global listofQuads
    global topScope



    for i in range(len(listofQuads)): 

        File.write('label%d: \n' % (listofQuads[i][0]))



        if (listofQuads[i][1] == '='): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('beq,t1,t2,label'+str(listofQuads[i][4])+'\n')
			
        elif (listofQuads[i][1] == '<'): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('blt,t1,t2,label'+str(listofQuads[i][4])+'\n')
			
        elif (listofQuads[i][1] == '>'): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('bgt,t1,t2,label'+str(listofQuads[i][4])+'\n')
			
        elif (listofQuads[i][1] == '<='): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('ble,t1,t2,label'+str(listofQuads[i][4])+'\n')
			
        elif (listofQuads[i][1] == '>='):
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('bge,t1,t2,label'+str(listofQuads[i][4])+'\n')
			
        elif (listofQuads[i][1] == '<>'): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('bne,t1,t2,label'+str(listofQuads[i][4])+'\n')
			
        elif (listofQuads[i][1] == 'JUMP'):
            File.write('b label'+str(listofQuads[i][4])+'\n')
			
        elif (listofQuads[i][1] == ':='): 
            loadvr(listofQuads[i][2],1)
            storerv(1,listofQuads[i][4])
			
        elif (listofQuads[i][1] == '+'): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('add,t1,t1,t2'+'\n')
            storerv(1,listofQuads[i][4])
			
        elif (listofQuads[i][1] == '-'): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('sub,t1,t1,t2'+'\n')
            storerv(1,listofQuads[i][4])
			
        elif (listofQuads[i][1] == '*'): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('mul,t1,t1,t2'+'\n')
            storerv(1,listofQuads[i][4])
			
        elif (listofQuads[i][1] == '/'): 
            loadvr(listofQuads[i][2],1)
            loadvr(listofQuads[i][3],2)
            File.write('div,t1,t1,t2'+'\n')
            storerv(1,listofQuads[i][4])
			
        elif (listofQuads[i][1] == 'inp'): 
            File.write('li a7,5'+'\n')
            File.write('ecall'+'\n')
            storerv(1,listofQuads[i][2])  
			
        elif (listofQuads[i][1] == 'out'): 
            loadvr(listofQuads[i][2],1)
            File.write('li a0'+'\n')
            File.write('li a7,1'+'\n') 
            File.write('ecall'+'\n')
			
        elif (listofQuads[i][1] == 'retv'): 
            loadvr(listofQuads[i][2],1)
            File.write('lw t0,-8(sp)\n')
            File.write('sw t1,(t0)\n')
    listofQuads = []

#sintaktikos analuths       
def syntax():
        global l #grammh
        global lexresult
        lexresult= lex()
        l = lexresult[2]

        def program():
                global l 
                global lexresult               
                if(lexresult[0] == program_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0] == id_tk):
                                id = lexresult[1]
                                lexresult = lex()
                                l = lexresult[2]
                                block(id,1)
                                if(lexresult[0] == full_stop_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        return
                                else:
                                        print("error:xriazete teleia gia na kleisei to program", l)
                                        exit(-1)
                        else:
                                print("error: den exei onoma to file/program",l)
                                exit(-1)
                else:
                         print("error: h lexh program den iparxei sthn arxh tou programatos",l)
                         exit(-1)
                        
        def block(name,flag):
                global lexresult
                
                if(lexresult[0] == l_block_tk):
                        lexresult = lex()
                        l = lexresult[2]

                        new_scope(name)
                        declarations()               
                        subprograms()
                        genQuad('begin_block',name,'_','_')
                        blockstatements()
                        if(flag==1):
                            genQuad('halt','_','_','_')
                        genQuad('end_block',name,'_','_')
                        if(flag!=1):
                                add_parameters()
                        if(lexresult[0] == r_block_tk):
                                lexresult = lex()
                                l = lexresult[2]

                                print("SYMBOL TABLE:")
                                print_symbol_table()
                                os.system("pause")
                                #final()
                                delete_scope()

                        else:
                                print('error: prepei na iparxei dexia aggili' , l)
                                exit(1)
                else:
                        print('error: prepei na iparxei aristeri aggili' , l)
                        return 
                                               
                
        def declarations():
                global lexresult                 
                while(lexresult[0] == declare_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        cfile.write("int ")
                        varlist()
                        cfile.write(";\n\t")
                        
                        if(lexresult[0] == questionmark_tk):
                                lexresult = lex()
                                l = lexresult[2]
                        else:
                                print("error: prepei na iparxei erwtimatiko sto telos tou varlist", l)
                                exit(-1)
                return
                                
        def varlist():
                global lexresult
                
                if(lexresult[0] == id_tk):
                        cfile.write(lexresult[1])
                        entity = Entity()
                        entity.type = 'VAR'
                        entity.name = lexresult[1]
                        new_entity(entity)
                        lexresult = lex()
                        l = lexresult[2]
                        while(lexresult[0] == comma_tk):
                                cfile.write(lexresult[1])
                                l = lexresult[2]
                                lexresult = lex()
                               
                                if(lexresult[0] == id_tk):
                                        cfile.write(lexresult[1])
                                        l = lexresult[2]
                                        entity = Entity()
                                        entity.type = 'VAR'
                                        entity.name = lexresult[1]
                                        new_entity(entity)
                                        lexresult = lex()
                                else:
                                        print("error: den exei komma prin to id", l)
                                        exit(-1)               
                return
                
        def subprograms():
                global lexresult               
                while(lexresult[0] == procedure_tk or lexresult[0] == function_tk ):

                        subprogram()
                return
                
                
        def subprogram():
                global lexresult               
                if(lexresult[0]==procedure_tk):
                        lexresult=lex()
                        l=lexresult[2]
                        
                        if(lexresult[0]==id_tk):
                                id = lexresult[1]
                                entity = Entity()
                                entity.name = lexresult[1]
                                entity.type = 'SUBPROGRAM'
                                entity.subprogram.type = 'Procedure'
                                new_entity(entity)
                                lexresult = lex()
                                l = lexresult[2]
                                if(lexresult[0] == l_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        formalparlist()                       
                                        if(lexresult[0] == r_parenthesis_tk):
                                                lexresult = lex()
                                                l = lexresult[2]
                                                block(id,0)                               
                                                return
                                        else:
                                                print("error: dexia parenthesei den klinei meta thn formalparlist",l)
                                                exit(-1)
                                else:
                                        print("error: aristerh parenthesi den anoigei prin thn formalparlist",l)
                                        exit(-1)
                        else:
                                print("error: prepei na iparxei id meta to procedure ", l)
                                exit(-1)
                elif(lexresult[0]== function_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0]==id_tk):
                                id = lexresult[1]
                                entity = Entity()
                                entity.name = lexresult[1]
                                entity.type = 'SUBPROGRAM'
                                entity.subprogram.type = 'Procedure'
                                new_entity(entity)
                                lexresult = lex()
                                l = lexresult[2]
                                if(lexresult[0] == l_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        formalparlist()                        
                                        if(lexresult[0] == r_parenthesis_tk):
                                                lexresult = lex()
                                                l = lexresult[2]
                                                block(id,0)                               
                                                return
                                        else:
                                                print("error: dexia parenthesei den klinei meta thn formalparlist",l)
                                                exit(-1)
                                else:
                                        print("error: aristerh parenthesi den anoigei prin thn formalparlist",l)
                                        exit(-1)
                        else:
                                print("error: prepei na iparxei id meta to function", l)
                                exit(-1)
                
        def formalparlist():
                global lexresult                
                formalparitem()                
                while(lexresult[0] == comma_tk):
                        lexresult  = lex()
                        l = lexresult[2]
                        formalparitem()                                
                return
                
        def formalparitem():
                global lexresult
                global l                
                if(lexresult[0] == in_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        arg = Argument()
                        arg.name = lexresult[1]
                        arg.parameterMode = 'CV'
                        new_argument(arg)
                        if(lexresult[0]== id_tk):

                                lexresult = lex()
                                l = lexresult[2]
                        else:
                                print("error: prepei na iparxei onoma metavlitis meta to 'in' ", l)
                                exit(-1)
                elif(lexresult[0] == in_out_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0] == id_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                arg = Argument()
                                arg.name = lexresult[1]
                                arg.parameterMode = 'REF'
                                new_argument(arg)
                                
                        else:
                                print("error: prepei na iparxei onoma metavlitis meta to 'inout' ", l)
                                exit(-1)
                else:
                        print("error:den iparxei 'in' oute 'inout'",l)
                        exit(-1)
                return
                        
                        
        def statements():
                global lexresult
                global l
                
                if(lexresult[0] == l_block_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        statement()                       
                        while(lexresult[0] == questionmark_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                statement()                               
                        if(lexresult[0] == r_block_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                return                               
                        else:
                                print("error: to block den kleinei sta statements", l)
                                exit(-1)
                else:
                        statement()
                        if(lexresult[0] == questionmark_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                return
                        else:
                                print("error: prepei na iparxei erotimatiko meta apo statement", l)
                                exit(-1)
                
        def blockstatements():
                global lexresult
                global l
                            
                statement()
                
                while(lexresult[0] == questionmark_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        statement()
                
        def statement():
                global lexresult
                
                if(lexresult[0]==id_tk):
                        assignment_stat()
                elif(lexresult[0]==print_tk):
                        print_stat()
                elif(lexresult[0]==if_tk):
                        if_stat()
                elif(lexresult[0]==while_tk):
                        while_stat()
                elif(lexresult[0]==switchcase_tk):
                        switchcase_stat()
                elif(lexresult[0]==forcase_tk):
                        forcase_stat()
                elif(lexresult[0]==incase_tk):
                        incase_stat()
                elif(lexresult[0]==call_tk):
                        call_stat()
                elif(lexresult[0]==return_tk):
                        return_stat()
                elif(lexresult[0]==input_tk):
                        input_stat()                
                return
                                      
        def assignment_stat():
                global lexresult
                
                if(lexresult[0] == id_tk):
                        id = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                        
                        if(lexresult[0] == assignment_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                Eplace = expression()
                                genQuad(':=', Eplace, '_', id)                            
                                return
                        else:
                                print("error: prepei na iparxei anathesi meta to onoma tis metavlitis.", l)
                                exit(-1) 
                else:
                        print("error:den uparxei id",l)
                        exit(-1)

        def if_stat():
                global lexresult
                global l
                
                if(lexresult[0] == if_tk):
                        lexresult= lex()
                        l = lexresult[2]
                        if(lexresult[0] == l_parenthesis_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                B = condition()
                                backPatch(B[0], nextQuad())                                
                                if(lexresult[0]== r_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        statements()
                                        ifList = makeList(nextQuad())
                                        genQuad('jump', '_', '_', '_')
                                        backPatch(B[1], nextQuad())
                                        elsepart()
                                        backPatch(ifList, nextQuad())
                                        return
                                else:
                                        print("error: den kleinei h parenthesi stin if", l)
                                        exit(-1)
                        else:
                                print("error: den exei anoiksei parenthesi stin if", l)
                                exit(-1)
                else:
                        print("error: provlima sto anoigma tis if",l)
                        exit(-1)               
                
        def elsepart():
                global lexresult
                global l
                
                if(lexresult[0] == else_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        statements()                       
                return               
                
        def while_stat():
                global lexresult
                global l
                
                if(lexresult[0]== while_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0] == l_parenthesis_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                Bquad=nextQuad()
                                B = condition()
                                backPatch(B[0], nextQuad())
                                if(lexresult[0] == r_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        statements()
                                        genQuad('jump', '_', '_', Bquad)
                                        backPatch(B[1], nextQuad())
                                        return
                                else:
                                        print("error: den kleinei swsta h parenthesi stin while", l)
                                        exit(-1)
                        else:
                                print("error: den anoigei swsta h parenthesi sthn while",l)
                                exit(-1)
                else:
                        print("error: provlima stin while", l)
                        exit(-1)

        def switchcase_stat():
                global lexresult
                global l
                
                if(lexresult[0] == switchcase_tk):
                        lexresult = lex()
                        l = lexresult[2]

                        exitList=emptyList()
                        while(lexresult[0] == case_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                if(lexresult[0] == l_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]

                                        Condition = condition()
                                        backPatch(Condition[0], nextQuad())
                                        if(lexresult[0] == r_parenthesis_tk):
                                                lexresult = lex()
                                                l = lexresult[2]
                                                statements()
                                                t = makeList(nextQuad())
                                                genQuad('jump', '_', '_', '_')
                                                exitList = mergeList(exitList, t)
                                                backPatch(Condition[1], nextQuad())
                                        else:
                                                print("error: prepei na iparxei deksia parenthesi sthn forcase", l)
                                                exit(-1)
                                else:
                                        print("error: prepei na iparxei aristeri parenthsi sthn forcase", l)
                                        exit(-1)
                        if(lexresult[0] == default_tk):
                                lexresult = lex()
                                l = lexresult[2]

                                statements()
                                backPatch(exitList, nextQuad())
                        else:
                                print("error: den arxizei swsta to default ths forcase", l)
                                exit(-1)
                else:
                        print("error: den arxizei swsta h forcase", l)
                        exit(-1)
        
        def forcase_stat():
                global lexresult
                global l
                
                if(lexresult[0] == forcase_tk):
                        lexresult = lex()
                        l = lexresult[2]

                        firstCondQuad=nextQuad()
                        while(lexresult[0] == case_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                if(lexresult[0] == l_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        Condition = condition()
                                        backPatch(Condition[0], nextQuad())                                       
                                        if(lexresult[0] == r_parenthesis_tk):
                                                lexresult = lex()
                                                l = lexresult[2]
                                                statements()

                                                genQuad('jump','_','_',firstCondQuad)
                                                backPatch(Condition[1], nextQuad())

                                        else:
                                                print("error: prepei na iparxei deksia parenthesi sthn forcase", l)
                                                exit(-1)
                                else:
                                        print("error: prepei na iparxei aristeri parenthsi sthn forcase", l)
                                        exit(-1)
                        if(lexresult[0] == default_tk):
                                lexresult = lex()
                                l = lexresult[2]

                                statements()
                        else:
                                print("error: den arxizei swsta to default ths forcase", l)
                                exit(-1)
                else:
                        print("error: den arxizei swsta h forcase", l)
                        exit(-1)
                
        def incase_stat():
                global lexresult
                global l
                
                if(lexresult[0] == incase_tk):
                        lexresult = lex()
                        l = lexresult[2]

                        flag = newTemp()
                        firstQuad=nextQuad()

                        genQuad(':=','0','_',flag)
                        while(lexresult[0] == case_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                if(lexresult[0] == l_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        Condition = condition()
                                        backPatch(Condition[0], nextQuad())                                       
                                        if(lexresult[0] == r_parenthesis_tk):
                                                lexresult = lex()
                                                l = lexresult[2]
                                                statements()

                                                genQuad(':=','1','_',flag)
                                                backPatch(Condition[1], nextQuad())
                                        else:
                                                print("error: prepei na iparxei deksia parenthesi sthn forcase", l)
                                                exit(-1)
                                else:
                                        print("error: prepei na iparxei aristeri parenthsi sthn forcase", l)
                                        exit(-1)
                        genQuad('=',flag,'1',firstQuad)
                else:
                        print("error: den arxizei swsta h forcase", l)
                        exit(-1)


        def call_stat():
                global lexresult
                global l
                
                if(lexresult[0] == call_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0] == id_tk):
                                assign_v = lexresult[1]
                                lexresult = lex()
                                l = lexresult[2]
                                if(lexresult[0] == l_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        actualparlist()
                                        genQuad('call', assign_v, '_', '_')
                                        if(lexresult[0] == r_parenthesis_tk):
                                                lexresult = lex()

                                                return
                                        else:
                                                print("error: prepei na kleinei h parenthesi sthn call",l)
                                                exit(-1)
                                else:
                                        print("error: prepei na anoigei parenthesi sthn call", l)
                                        exit(-1)                               
                        else:
                                print("error: prepei yparxei id sthn call", l)
                                exit(-1)
                else:
                        print("error: den arxizei swsta h call",l)
                        exit(-1)               
                return

        def return_stat():
                global lexresult
                global l
                
                if(lexresult[0] == return_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0] == l_parenthesis_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                Eplace = expression()
                                genQuad('retv', Eplace, '_', '_')                             
                                if(lexresult[0] == r_parenthesis_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        return
                                else:
                                        print("error: prepei na kleinei h parenthesi sthn return",l)
                                        exit(-1)
                        else:
                                print("error: prepei na anoigei parenthesi sthn return", l)
                                exit(-1)                
                
        
                
        def print_stat():
                global lexresult
                global l
                
                if(lexresult[0] == print_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0] == l_parenthesis_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                Eplace = expression()
                                genQuad('out', Eplace, '_', '_')                               
                                if(lexresult[0] == r_parenthesis_tk):
                                        lexresult = lex()
                                      
                                else:
                                        print("error: prepei na kleinei h parenthesi sthn print",l)
                                        exit(-1)
                        else:
                                print("error: prepei na anoigei parenthesi sthn print", l)
                                exit(-1)
                else:
                        print("error: den arxizei swsta h print", l)
                        exit(-1)
                return
                
        def input_stat():
                global lexresult
                global l
                
                if(lexresult[0] == input_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0] == l_parenthesis_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                if(lexresult[0] == id_tk):
                                        id = lexresult[1]
                                        genQuad('inp',id,'_','_')
                                        lexresult = lex()
                                        l = lexresult[2]
                                        if(lexresult[0] == r_parenthesis_tk):
                                                lexresult = lex()
                                                l = lexresult[2]
                                                return                                               
                                        else:
                                                print("error: prepei na kleinei h parenthesi stin input",l)
                                                exit(-1)
                                else:
                                        print("error: prepei na iparxei id stin input",l)
                                        exit(-1)
                        else:
                                print("error: prepei na anoigei parenthesi sthn input", l)
                                exit(-1)
                else:
                        print("error: den arxizei swsta h input", l)
                        exit(-1)

        def actualparlist():
                global lexresult
                global l                 
                actualparitem()
                
                while(lexresult[0] == comma_tk):
                        lexresult  = lex()
                        l = lexresult[2]
                        actualparitem()                       
                return
                
        def actualparitem():
                global lexresult
                global l
                
                if(lexresult[0] == in_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        a = expression()
                        genQuad('par', a, 'CV', '_')                       
                elif(lexresult[0] == in_out_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        if(lexresult[0] == id_tk):

                                b = lexresult[1]
                                lexresult = lex()
                                l = lexresult[2]
                                genQuad('par',b, 'REF', '_')
                        else:
                                print("error: prepei na iparxei onoma metavlitis meta to 'inout' ", l)
                                exit(-1)    
                else:
                        print("error:den iparxei 'in' oute 'inout'",l)
                        exit(-1)
                return               
                
        def condition():
                global lexresult
                global l                
                Btrue = []
                Bfalse = []
                Q1 = boolterm()
                Btrue = Q1[0]
                Bfalse = Q1[1]
                
                while(lexresult[0]==or_tk):
                        lexresult=lex()
                        l = lexresult[2]
                        backPatch(Bfalse, nextQuad())                       
                        Q2 = boolterm()
                        Btrue = mergeList(Btrue, Q2[0])
                        Bfalse = Q2[1]
                return Btrue, Bfalse
                                
        def boolterm():
                global lexresult
                global l                
                Qtrue = []
                Qfalse = []

                R1 = boolfactor()
                Qtrue = R1[0]
                Qfalse = R1[1]
                while(lexresult[0]==and_tk):
                        lexresult=lex()
                        l = lexresult[2]

                        backPatch(Qtrue, nextQuad())
                        R2 = boolfactor()
                        Qfalse = mergeList(Qfalse, R2[1])
                        Qtrue = R2[0]
                return Qtrue, Qfalse
                
        def boolfactor():
                global lexresult
                global l
                Rtrue = []
                Rfalse = []
                
                if(lexresult[0]==not_tk):
                        lexresult=lex()
                        l = lexresult[2]
                        
                        if(lexresult[0]==l_bracket_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                B = condition()                               
                                if(lexresult[0]==r_bracket_tk):
                                        lexresult = lex()
                                        l = lexresult[2]
                                        Rtrue = B[1]
                                        Rfalse = B[0]
                                else:
                                        print("error: prepei na iparxei kleisimo agkylis meta tin  boolfactor ",l)
                                        exit(-1)
                        else:
                                print("error: xriazetai anoigma agkylis meta to not stin boolfactor", l)
                                exit(-1)
                elif(lexresult[0]==l_bracket_tk):
                        lexresult = lex()
                        l = lexresult[2]
                        B = condition()                        
                        if(lexresult[0]==r_bracket_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                Rtrue = B[0]
                                Rfalse = B[1]
                        else:
                                print("error:  prepei na iparxei kleisimo agkylis meta tin  boolfactor", l)
                                exit(-1)
                else:
                        
                        Eplace1 = expression()
                        relop = relational_op()
                        Eplace2 = expression()
                        Rtrue=makeList(nextQuad())
                        genQuad(relop, Eplace1, Eplace2, '_')
                        Rfalse=makeList(nextQuad())
                        genQuad('jump', '_', '_', '_')

                return Rtrue,Rfalse
                                
        def expression():
                global lexresult
                global l
                
                optional_sign()                
                T1place = term()               
                while(lexresult[0]==plus_tk or lexresult[0]==minus_tk):
                        plusminus = add_op()
                        T2place = term()                                             
                        w = newTemp()
                        genQuad(plusminus, T1place, T2place, w)
                        T1place = w
                Eplace = T1place
                return Eplace                        
                
        def term():
                global lexresult
                global l   
                F1place = factor()
                while(lexresult[0]==multiply_tk or lexresult[0]==divide_tk):
                        mulsym = mul_op()
                        F2place = factor()
                        w=newTemp()
                        genQuad(mulsym, F1place, F2place, w)
                        F1place = w
                Tplace =F1place
                return Tplace
                                
        def factor():
                global lexresult
                global l
                
                if(lexresult[0]==num_tk):
                        Fplace= lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                elif(lexresult[0]==l_parenthesis_tk):
                        lexresult = lex()
                        l = lexresult[2]
                         
                        Eplace = expression()
                        Fplace = Eplace                       
                        if(lexresult[0]==r_parenthesis_tk):
                                lexresult = lex()
                                l = lexresult[2]
                        else:
                                print("error: xriazetai dexia parenthesi  meta to expression stin factor ",l)
                                exit(-1)
                elif(lexresult[0]==id_tk):
                        Fplacetemp = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                        Fplace=idtail(Fplacetemp)
                else:
                        print("error: xriazetai constant h expression h variable stin factor",l)
                        exit(-1)               
                return Fplace               
        
        def idtail(assign_v):
                global lexresult
                global l
                
                if(lexresult[0] == l_parenthesis_tk ):
                        lexresult = lex()
                        l = lexresult[2]
                        actualparlist()
                        w=newTemp()
                        genQuad('par', w, 'RET', '_')
                        genQuad('call', assign_v, '_', '_')
                        if(lexresult[0]==r_parenthesis_tk):
                                lexresult = lex()
                                l = lexresult[2]
                                return w
                        else:
                                print("error: xriazete dexia parenthesi  meta to actualparlist sto idtail ",l)
                                exit(-1)
                else:
                        return assign_v

        def optional_sign():
                global lexresult
                global l
                
                if(lexresult[0] == plus_tk or lexresult[0] == minus_tk):                        
                        add_op()                        
                return
                
        def relational_op():
                global lexresult 
                global l
                
                if(lexresult[0]==equal_tk):
                        relop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                elif(lexresult[0]==diff_tk):
                        relop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                elif(lexresult[0]== greater_than_tk):
                        relop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                elif(lexresult[0]==greater_or_equal_tk):
                        relop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                elif(lexresult[0]==less_than_tk):
                        relop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                elif(lexresult[0]==less_or_equal_tk):
                        relop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2] 
                else:
                        print("error: den iparxei = , < , <= , <> , >= , > ",l)
                        exit(-1)
                return relop
                
        def add_op():
                global lexresult 
                global l
                
                if(lexresult[0]==plus_tk):
                        addop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                elif(lexresult[0]==minus_tk):  
                        addop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                return  addop

        def mul_op():
                global lexresult 
                global l
                
                if (lexresult[0] == multiply_tk):
                        mulop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                elif (lexresult[0] == divide_tk):
                        mulop = lexresult[1]
                        lexresult = lex()
                        l = lexresult[2]
                return mulop

        program()

        return


def cCode():
    cfile.write("int ")

    for i in range(len(tempvariablelist)): 
        cfile.write(tempvariablelist[i])
        if(len(tempvariablelist) == i+1):
            cfile.write(";\n\t")
        else:
            cfile.write(",")
    for j in range(len(listofQuads)):
        if(listofQuads[j][1] == 'begin_block'):
            cfile.write("L_"+str(j+1)+":\n\t")
        elif(listofQuads[j][1] == ":="):
            cfile.write("L_"+str(j+1)+": "+ listofQuads[j][4]+"="+listofQuads[j][2]+";\n\t")
        elif((listofQuads[j][1] == "+") or (listofQuads[j][1] == "-") or (listofQuads[j][1] == "*")or(listofQuads[j][1] == "/")):
            cfile.write("L_"+str(j+1)+": "+ listofQuads[j][4]+"="+listofQuads[j][2]+"+"+listofQuads[j][3]+";\n\t")
        elif(listofQuads[j][1] == "jump"):
            cfile.write("L_"+str(j+1)+": "+"goto L_"+str(listofQuads[j][4])+ ";\n\t")
        elif((listofQuads[j][1] == "=") or (listofQuads[j][1] == "<") or (listofQuads[j][1] == ">") or (listofQuads[j][1] == ">=") or (listofQuads[j][1] == "<=") or (listofQuads[j][1] == "<>")):
            cfile.write("L_"+str(j+1)+": "+"if ("+listofQuads[j][2]+"<"+listofQuads[j][3]+") goto L_"+str(listofQuads[j][4])+";\n\t")
        elif(listofQuads[j][1] == "out"): 
            cfile.write("L_"+str(j+1)+": "+"printf(\""+listofQuads[j][2]+"= %d\", "+listofQuads[j][2]+");\n\t")
        elif(listofQuads[j][1] == 'halt'):
            cfile.write("L_"+str(j+1)+": {}\n\t")


def intCode(intfile):
    for i in range(len(listofQuads)):
        q = listofQuads[i]
        intfile.write(str(q[0]) + ":  " + str(q[1]) + ":  " + str(q[2]) + ":  " + str(q[3]) + ":  " + str(q[4]) +  "\n")





def files():
        global cfile

        cfile = open('cfile.c', 'w')
        cfile.write("int main(){\n\t")
        syntax()
        cCode()
        cfile.write("\n}")
        cfile.close()

        intfile = open('intfile.int', 'w')
        intCode(intfile)
        intfile.close()
        File.close()
files()


def printlistofquads():
    for i in range(len(listofQuads)):
        print (str(listofQuads[i][0])+" "+str(listofQuads[i][1])+" "+str(listofQuads[i][2])+" "+str(listofQuads[i][3])+" "+str(listofQuads[i][4]))
printlistofquads()
