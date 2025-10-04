#%%
from formula import *
import re
from io import  TextIOWrapper

#%%
class __read_buf:
    data:str=""

def get_char(file:TextIOWrapper)->str:
    if __read_buf.data:
        c=__read_buf.data
        __read_buf.data=""
        return c
    return file.read(1);

def put_char(c:str)->None:
    __read_buf.data=c
        
def is_blank(s:str)->bool:
    obj=re.match("^[ \n]*$",s)
    return bool(obj)

def get_word(file:TextIOWrapper)->str:
    l:list[str]=[];
    c:str=get_char(file);
    if c=="":
        return ""
    while is_blank(c):
        c:str=get_char(file);
        if c=="":
            return ""
    if c in ["(",")"]:
        return c;
    while not (is_blank(c) or c in ["(",")"]):
        l.append(c);
        c:str=get_char(file);  
    if c in ["(",")"]:
        put_char(c)
    return "".join(l);
#%%
def read_pop(file:TextIOWrapper)->None:
    i:int=1;
    while  i!=0:
        s:str=get_word(file)
        # # print(s,end="")
        if s=="(":
            i+=1;
        if s==")":
            i-=1;
        if s=="":
            return
#%%
def read_formula_let(file:TextIOWrapper,vdict)->formula:
    s:str=get_word(file)
    vdict1:dict[str,formula]=vdict.copy()
    assert s=="(","read_formula_let 非法输入%s"% s;
    while True:
        s:str=get_word(file)
        if s==")":
            break
        assert s=="(","read_formula_let 非法输入%s"% s;
        var:str=get_word(file)
        assert not(var in ["(",")"]),"read_formula_let 非法输入%s"% s;
        f:formula=read_formula(file,vdict)
        vdict1[var]=f
        s:str=get_word(file)
        assert s==")","read_formula_let 非法输入%s"% s;
    f=read_formula(file,vdict1)
    s:str=get_word(file)
    assert s==")","read_formula_let 非法输入%s"% s;
    return f;
def read_formula(file:TextIOWrapper,vdict,fs=None)->formula:
    if fs:
        s:str=fs
    else:
        s:str=get_word(file)
    if s!="(":
        if s in vdict:
            return vdict[s]
        try:
            return formula_int(int(s))
        except:
            pass
        try:
            return formula_float(float(s))
        except:
            pass
        raise IOError("read_formula 非法输入%s" % s);
    s:str=get_word(file)
    if s=="let":
        return read_formula_let(file,vdict);
    if not(s in ["+","-","*","/","and","or","not",">","<","<=",">=","="]):
        # print("%s" % s)
        raise IOError("read_formula 非法输入%s" % s);
    op=s;
    l=[];
    s:str=get_word(file)
    while s!=")":
        assert s,"read_formula 非法输入%s" % s
        l.append(read_formula(file,vdict,s))
        s:str=get_word(file)
    return apply(op,l)
#%%
class smtlib:
    def __init__(self) -> None:
        self.vars=[];
        self.var_dict=dict();
        self.set_info=dict();
        self.assert_list=[];

def read_declare_fun(slib:smtlib,file:TextIOWrapper)->None:
    s:str=get_word(file)
    assert not s in ['(',')'], "read_declare_fun 非法输入%s"% s
    var=s;
    s:str=get_word(file)
    assert  s in ['('], "read_declare_fun 非法输入%s"% s
    s:str=get_word(file)
    assert  s in [')'], "read_declare_fun 非法输入%s"% s
    s:str=get_word(file)
    s:str=get_word(file)
    assert  s in [')'], "read_declare_fun 非法输入%s"% s
    f=formula_var(var);
    slib.vars.append(f);
    slib.var_dict[var]=f;
    # # print("add var:",var)
def read_declare_const(slib:smtlib,file:TextIOWrapper)->None:
    s:str=get_word(file)
    assert not s in ['(',')'], "read_declare_fun 非法输入%s"% s
    var=s;
    # s:str=get_word(file)
    # assert  s in ['('], "read_declare_fun 非法输入%s"% s
    # s:str=get_word(file)
    # assert  s in [')'], "read_declare_fun 非法输入%s"% s
    s:str=get_word(file)
    s:str=get_word(file)
    assert  s in [')'], "read_declare_fun 非法输入%s"% s
    f=formula_var(var);
    slib.vars.append(f);
    slib.var_dict[var]=f;
def read_set_info(slib:smtlib,file:TextIOWrapper)->None:
    s:str=get_word(file)
    if s in [":smt-lib-version", ":category",":status" ]:
        s1:str=get_word(file);
        assert not s1 in ['(',')'], "read_set_info 非法输入%s"% s1
        slib.set_info[s]=s1
        # print("read_set_info:",s,s1)
        s:str=get_word(file)
        assert  s in [')'], "read_declare_fun 非法输入%s"% s
        return
    # print("read_set_info: unknow set_info %s" % s)
    read_pop(file);
def read_set_logic(slib:smtlib,file:TextIOWrapper)->None:
    s1:str=get_word(file);
    assert not s1 in ['(',')'], "read_set_logic 非法输入%s"% s1
    slib.set_info["set_logic"]=s1
    # print("read_set_logic:",s1)
    s:str=get_word(file)
    assert  s in [')'], "read_declare_fun 非法输入%s"% s
def read_annotation(file:TextIOWrapper)->None:
    file.readline()
def read_assert(slib:smtlib,file:TextIOWrapper)->None:
    # # print("read_assert",end=" ")
    f:formula=read_formula(file,slib.var_dict)
    # # print(f,end=" ")
    slib.assert_list.append(f)
    s:str=get_word(file)
    # # print(".")
    assert  s in [')'], "read_declare_fun 非法输入%s"% s
def read_smtlib2(file:TextIOWrapper)->smtlib:
    ans=smtlib()
    s:str=get_word(file)
    while s:
        # print("s: ",s)
        anno_flag=False
        assert s=='(' or s==';' or s==";;", "read_smtlib2 非法输入%s"% s
        if s==';':
            anno_flag=True
        s=get_word(file)
        if s==")":
            s=get_word(file)
            continue
        funl={
            "declare-fun":read_declare_fun,
            "declare-const":read_declare_const,
            "set-info":read_set_info,
            "set-logic":read_set_logic,
            "assert":read_assert
        }
        if s in funl:
            funl[s](ans,file)
        elif anno_flag:
            read_annotation(file)
        else:
            # print("read_smtlib2: unknow  %s" % s)
            read_pop(file);
        s:str=get_word(file)
    return ans;
#%%
# a:TextIOWrapper=open("../example/smt_lib_file/matrix-1-all-2.smt2","r")
# slib=read_smtlib2(a)
# a:TextIOWrapper=open("../example/smt_lib_file/C_3_64.smt2","r")
# slib=read_smtlib2(a)
# %%
