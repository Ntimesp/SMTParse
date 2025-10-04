#%%
from typing import Any
from smt_lib_parse import smtlib
from formula import *
from func_op import *
#%%
def formula_int_op(f:formula_int,vdict,beta:float=0):
    return lambda x:int(f)
def formula_float_op(f:formula_float,vdict,beta:float=0):
    return lambda x:float(f)
def formula_var_op(f:formula_var,vdict,beta:float=0):
    i=vdict[str(f)]
    return lambda x:x[i]

def formula_add_op(f:formula_float,vdict,beta:float=0):
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    return func_add(l)
def formula_sub_op(f:formula_float,vdict,beta:float=0):
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    return func_sub(l)
def formula_mul_op(f:formula_float,vdict,beta:float=0):
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    return func_mul(l)
def formula_div_op(f:formula_float,vdict,beta:float=0):
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    return func_div(l)


def formula_l_op(f:formula_float,vdict,beta:float=0):#<
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    assert len(l)==2, "formula_l_op: 意外输入 %s" % str(f)
    return func_l(l[0],l[1],beta) 
def formula_le_op(f:formula_float,vdict,beta:float=0):#<
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    assert len(l)==2, "formula_l_op: 意外输入 %s" % str(f)
    return func_le(l[0],l[1],beta) 
def formula_g_op(f:formula_float,vdict,beta:float=0):#<
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    assert len(l)==2, "formula_l_op: 意外输入 %s" % str(f)
    return func_l(l[1],l[0],beta) 
def formula_ge_op(f:formula_float,vdict,beta:float=0):#<
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    assert len(l)==2, "formula_l_op: 意外输入 %s" % str(f)
    return func_le(l[1],l[0],beta) 
def formula_eq_op(f:formula_float,vdict,beta:float=0):#<
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    assert len(l)==2, "formula_l_op: 意外输入 %s" % str(f)
    return func_eq(l[0],l[1],beta) 

def formula_and_op(f:formula_float,vdict,beta:float=0):
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    return func_add(l)
def formula_or_op(f:formula_float,vdict,beta:float=0):
    l=list(map(lambda f1:formula_op(f1,vdict,beta),f.get_ele()))
    return func_mul(l)
def formula_not_op(f:formula_float,vdict,beta:float=0):
    # print("f: ",f)
    assert len(f.get_ele())==1, "formula_l_op: 意外输入 %s" % str(f)
    f1=formula_apply_not(f[0])
    # print("f1: ",f1)
    return formula_op(f1,vdict,beta)

def formula_op(f:formula,vdict,beta:float=0):
    head:str=f.get_head()
    l={
        "int":formula_int_op,
        "float":formula_float_op,
        "var":formula_var_op,
        "+":formula_add_op,
        "-":formula_sub_op,
        "*":formula_mul_op,
        "/":formula_div_op,
        "<":formula_l_op,
        "<=":formula_le_op,
        ">":formula_g_op,
        ">=":formula_ge_op,
        "==":formula_eq_op,
        "=":formula_eq_op,
        "and":formula_and_op,
        "or":formula_or_op,
        "not":formula_not_op
    }
    if head in l:
        return l[head](f,vdict,beta)
    else:
        raise  Exception("formula_op: unknown op %s: %s" % (f.get_head(),str(f)))

#%%
def smt_op(slib:smtlib,beta:float=0):
    f=apply("and",slib.assert_list)
    vdict=dict()
    for i in range(len(slib.vars)):
        vdict[str(slib.vars[i])]=i
    return formula_op(f,vdict,beta)
    


# %%
