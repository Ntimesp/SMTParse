#%%
import sys
import os
sys.path.append(os.path.abspath('../lib/smtlib_parse'))
sys.path.append(os.path.abspath('smt_python_parse/src'))
#%%
from smt_op import *
from smt_lib_parse import *
a:TextIOWrapper=open("Sexample/test/C_3_64.smt2","r")
slib=read_smtlib2(a)
f=smt_op(slib,0)
xd={
"x6":    (1.0/4.0),
"x13":    1.0,
"x3":    3.0,
"x10":    (1.0/4.0),
"x0":    1.0,
"x7":    (1.0/2.0),
"x4":    1.0,
"x11":    (1.0/16.0),
"x1":    1.0,
"x8":    2.0,
"x5":    (1.0/2.0),
"x12":    (1.0/8.0),
"x2":    1.0,
"x9":    1.0
}
xd={
"x6": 1.0,
"x13": 1.0,
"x3": 1.0,
"x10": 1.0,
"x0": 1.0,
"x7": 1.0,
"x4": 1.0,
"x11": 1.0,
"x1": 1.0,
"x8": 1.0,
"x5": 1.0,
"x12": 1.0,
"x2": 1.0,
"x9":    1.0
}

x=list(map(lambda f:xd[str(f)],slib.vars))
print(f(x))
#%%
import numpy as np
from scipy.optimize import basinhopping
import random 
import time
#%%
time_b=time.time()
a:TextIOWrapper=open("/home/wyl/git-repo/fsmt_test/ylWu/Case/QF_NRA/20170501-Heizmann-UltimateInvariantSynthesis/hhk2008.c.i_3_3_2.bpl_5.smt2","r")
slib=read_smtlib2(a)
time_e=time.time()
time_consume=time_e-time_b
print(time_consume)
#%%
time_b=time.time()
f=smt_op(slib,1e-6)
time_e=time.time()
time_consume=time_e-time_b
print(time_consume)

#%%
class tmp:
    index:int=0;
def callback(x, f, accept):
    tmp.index+=1;
    print("%d: %f" % (tmp.index,f))
    return f==0 
var_num=len(slib.vars)

x=np.zeros(var_num) # 待求解的变元list
for i in range(var_num):
    x[i]=random.uniform(-100.0,100.0)

time_b=time.time()
f(x)
time_e=time.time()
time_consume=time_e-time_b
print(time_consume)

#%%
time_b=time.time()
minimizer_kwargs = {"method":"Powell"}
tmp.index=0
ret1 = basinhopping(f, x, minimizer_kwargs=minimizer_kwargs,niter=200,callback=callback)
time_e=time.time()
time_consume=time_e-time_b
print(time_consume)
print(ret1.x)
print(f(ret1.x))
# %%
