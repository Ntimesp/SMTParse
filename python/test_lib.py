
#%% 
import os
import sys
sys.path.append(os.path.abspath('../lib/smtlib_parse'))
import NRA_op

#%%
A=NRA_op.NRA_op("../benchmark/non-incremental/QF_NRA/20161105-Sturm-MBO/mbo_E1.smt2")
# %%
vs=A.vars()
print(len(vs))
#%%
vs[0]
#%%
print(A.len())
print(A.C_len(0))
print(A.get_atom_str(0,0))
#%% 
print(A.str())
#%%
A=NRA_op.NRA_op("/home/ker/Documents/smt-work/QF_NRA/LassoRanker/CooperatingT2/collatz.t2.c_Iteration1_Loop_4-pieceTemplate.smt2",True)
# %%
vs=A.vars()
print(len(vs))
#%%
vs[0]
#%%
print(A.len())
print(A.C_len(0))
print(A.get_atom_str(0,0))
#%% 
print(A.str())
# %%
# double dl_B=0,double dl_a=0,double deq_B=0,double deq_a=0
# /*
#     assign(A && B)=assign(A)+assign(B);
#     assign(A || B)=assign(A)*assign(B);
#     assign(f>0)={
#         (assign(f)>dl_B)? 0 :(assign(f)-dl_B)^2+ dl_a;
#     };
#     assign(f==0)={
#         (assign(f)>deq_B)? (assign(f)-deq_B)^2+ deq_a
#             :(
#                 (assign(f)<-deq_B)?(assign(f)+deq_B)^2+ deq_a:0
#             )
#     };
#     assign(f<0)={
#         (assign(f)<-dl_B)? 0 :(assign(f)+dl_B)^2+ dl_a;
#     };
# */
import time
x=[0]*len(vs);
t=time.time();
A.op(x,0,0,0,0)
print(time.time()-t)
# %%
#%%
from scipy.optimize import basinhopping
import time
import random 
import numpy as np
#%%
var_num=len(A.vars())
f=lambda x: A.op(x.tolist(),0,0,0,0)
x=np.zeros(var_num) # 待求解的变元list
for i in range(var_num):
    x[i]=random.uniform(-100.0,100.0)

time_b=time.time()
f(x)
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

time_b=time.time()
minimizer_kwargs = {"method":"Powell"}
ret1 = basinhopping(f, x, minimizer_kwargs=minimizer_kwargs,niter=200,callback=callback)
time_e=time.time()
time_consume=time_e-time_b
print(time_consume)
print(ret1.x)
print(f'{f(ret1.x) :.9e}')
# %%
