#!/usr/bin/python3
#%%
from SMTParse.python.runmaple.run_test import test_data_lib
import re
import os
import argparse
import matplotlib.pyplot as plt
from math import ceil

#%%

def get_op_name(s:str)->str:
    D={"maple":"LS","z3":"Z3","cvc5":"CVC5","yices-smt2":"Yices2","mathsat":"MathSAT5","maple-cvc5":"LS+CVC5"}
    if s in D:
        return D[s]
    return s
def get_ex_name(s:str)->str:
    # maple_mode=r'"?(\./)?([^"\']*result2?/)?(?P<name>(random_ex_test)?[^"\']*)\.smt2\.mpl"?'
    # obj=re.match(maple_mode,s)
    # if obj:
    #     name=obj.group("name")
    #     # print(name)
    #     return name
    
    rm_mode=r'"?((\./)|([^"\']*QF_NRA/)|([^"\']*result2?/))(?P<name>[^"\']*)\.smt2(.mpl)?"?'
    obj=re.match(rm_mode,s)
    if obj:
        name=obj.group("name")
        # print(name)
        return name

    random_mode=r'"?([^"\']*random_ex_test/)(?P<name>[^"\']*)\.smt2(.mpl)?"?'
    obj=re.match(random_mode,s)
    if obj:
        name="random_ex_test/"+obj.group("name")
        return name
    random_mode2=r'"?(?P<name>random_ex_test/random_ex_test[0-9]*)"?'
    obj=re.match(random_mode2,s)
    if obj:
        name=obj.group("name")
        return name
    
    raise Exception("no name")
    # return ""
def read_list(file_name:str)->list[str]:
    with open(file_name,"r") as f:
        ans:list[str]=[]
        for i in f:
            mode=r'"(?P<name>[^"]*)"\s*,\s*(?P<index>[0-9])'
            obj=re.match(mode,i)
            if (obj and obj.group("index")=="0"):
                ans.append(get_ex_name(obj.group("name")))
        return ans;

def read_csv(lib:test_data_lib,file_name:str)->None:
    with open(file_name,"r") as f:
        for i in f:
            mode=r'\s*(?P<name>[^,\s]*)\s*,\s*(?P<op>[^,\s]*)\s*,\s*(?P<ans>[^,\s]*)\s*,\s*(?P<time>[^,\s]*)\s*'
            obj=re.match(mode,i)
            if obj:
                name=get_ex_name(obj.group("name"))
                op=obj.group("op")
                ans=obj.group("ans")
                t=float(obj.group("time"))
                lib.add_data_com(name,op,ans,t); 
            else:
                print(i)
                # return name
# def read_maple_data(lib,s:str)
def read_maple_txt(lib:test_data_lib,file_name:str)->None:
    with open(file_name,"r") as f:
        s=f.read();
        for i in s.split("###"):
            mode=r'\s*([0-9]*)\s*,\s*\["(?P<name>[^,\s]*)"\]\s*'
            obj=re.search(mode,i)
            if obj:
                name=get_ex_name(obj.group("name"))
                op="maple"
                ans="unknown"
                t=-1
                mode_sat=r"The CNF formula is satisfiable."
                obj_sat=re.search(mode_sat,i)
                if obj_sat:
                    ans="sat"
                    assert(i.find("CnfResult: true")>=0)
                mode_time=r"TotalTime: (?P<time>\S*)"
                obj_time=re.search(mode_time,i)
                if obj_time:
                    t=float(obj_time.group("time"))      
                lib.add_data_com(name,op,ans,t); 
            
            else:
                print(i)
def read_maple_dir(lib:test_data_lib,dir_name:str)->None:
    for (roots,dirs,files) in os.walk(dir_name):
        for file_name_ in  files:
            file_name=os.path.join(roots,file_name_)
            if len(file_name)<=3 or file_name[-4:]!=".log":
                continue
            with open(file_name,"r") as f:
                i=f.read()
                mode=r'\s*([0-9]*)\s*,\s*\["(?P<name>[^,\s]*)"\]\s*'
                obj=re.search(mode,i)
                if obj:
                    name=get_ex_name(obj.group("name"))
                    op="maple"
                    ans="unknown"
                    t=-1
                    mode_sat=r"The CNF formula is satisfiable."
                    obj_sat=re.search(mode_sat,i)
                    if obj_sat:
                        ans="sat"
                        assert(i.find("CnfResult: true")>=0)
                    mode_time=r"TotalTime: (?P<time>\S*)"
                    obj_time=re.search(mode_time,i)
                    if obj_time:
                        # if obj_time.group("st"):
                        #     print("++ ",file_name)
                        #     print(obj_time)
                        #     # print(obj_time.group("st"))
                        st=obj_time.group("time")
                        if (len(st)>=3 and st[-3:]=="-st"):
                            print("++ ",file_name)
                            print(obj_time)
                            st=st[:-3]
                        t=float(st)      
                    lib.add_data_com(name,op,ans,t); 
                
                else:
                    print(i)
def get_table(lib:test_data_lib,op:list[str]):
    def get_index(s):
        if (s.find("random")>=0):
            return 1
        else:
            return 0
    n=2;
    
    ans=[]
    smo=[0]*len(op)
    tt=[0]*n
    for i in range(len(op)):
        ans.append([0]*n)
    for i in lib.get_ex_list():
        index=get_index(i)
        tt[index]+=1
        for j in range(len(op)):
            if lib.get_data(i,op[j])[0]=="sat":
                ans[j][index]+=1
            if lib.get_data(i,op[j])[1]<=1:
                smo[j]+=1
            
    print(",num,",",".join(op))
    print("smt-lib,",tt[0],",",",".join(map(lambda x:str(x[0]),ans)))
    print("random,",tt[1],",",",".join(map(lambda x:str(x[1]),ans)))
    print("<1s,",",",",".join(map(str,smo)))
    print("total,",sum(tt),",".join(map(lambda x:str(sum(x)),ans)))

def get_compared_table(lib:test_data_lib,op1:str,op2:str):
    dir_name=["random"]
    def get_ex_lib_name(s:str):
        if s.find("random")>=0:
            return "random"
        else:
            tmp=s.split("/")
            assert(len(tmp)>=1)
            return tmp[0]
    def get_index(s:str):
        tmp=get_ex_lib_name(s)
        if tmp in dir_name:
            return dir_name.index(tmp)
        else:
            op1_w.append(0);
            op2_w.append(0);
            dir_name.append(tmp)
            return len(dir_name)-1

    op1_w=[0]*len(dir_name)
    op2_w=[0]*len(dir_name)
    
    for i in  lib.get_ex_list():
        index=get_index(i)
        if lib.get_data(i,op1)[0]=="sat":
            if lib.get_data(i,op2)[0]=="sat":
                if lib.get_data(i,op1)[1]<lib.get_data(i,op2)[1]:
                    op1_w[index]+=1
                else:
                    op2_w[index]+=1
            else:
                op1_w[index]+=1
        elif lib.get_data(i,op2)[0]=="sat":
            op2_w[index]+=1
    
    print(f"name,{get_op_name(op1)},{get_op_name(op2)}")
    for i in dir_name:
        print(i,",",op1_w[dir_name.index(i)],",",op2_w[dir_name.index(i)])

def polt_line(lib:test_data_lib,op:list[str]):
    fig, ax = plt.subplots(1, 1, sharex=True, constrained_layout=True)
    
    step=0.01;
    x=list(range(0,int(1200/step)+1))
    c=[]
    y=[]
    for i in range(len(x)):
        x[i]*=step
    for i in range(len(op)):
        c.append([0]*len(x))
        y.append([0]*len(x))
    for i in lib.get_ex_list():
        for j in range(len(op)):
            if lib.get_data(i,op[j])[0] in ["sat","unsat"]:
                c[j][int(lib.get_data(i,op[j])[1]/step)]+=1
    for i in range(len(op)):
        tmp=0;
        for j in range(len(x)):
            tmp+=c[i][j]
            y[i][j]=tmp
    fig, ax = plt.subplots(1, 1, sharex=True, constrained_layout=True)
    for i in range(len(op)):
        ax.plot(x[:-1], y[i][:-1], label=get_op_name(op[i]))
    # ax.set_facecolor('0.6')
    ax.set_xscale('log')
    ax.legend(loc='lower right')
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('solved instances')
    fig.show()
    fig.savefig("all_compared_line.pdf")
def polt_Compared(lib:test_data_lib,op1:str,op2:str):
    plt.rcParams['date.converter'] = 'concise'
    
    fig, ax = plt.subplots(1, 1, sharex=True, constrained_layout=True)
    lop1=[];
    lop2=[];
    ll=[];
    for i in lib.get_ex_list():
        lop1.append(lib.get_data(i,op1)[1])
        lop2.append(lib.get_data(i,op2)[1])
        ll.append((lop1[-1]+1)/(lop2[-1]+1))
    # ax.set_facecolor('0.6')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot([0.001,1200], [0.001,1200],linestyle="dotted",color="grey")
    sc = ax.scatter(lop1, lop2,s=4)
    ax.set_xlabel(f'{get_op_name(op1)} [sec]')
    ax.set_ylabel(f'{get_op_name(op2)} [sec]')
    # ax.set_title('Comparing_', loc='left')
    # fig.colorbar(sc, ax=ax, shrink=0.6, label='day of year')
    fig.show()
    fig.savefig(f"Comparing_{op1}_{op2}.pdf")
    # this changes the default date converter for better interactive plotting of dates:
    
#%%
if __name__=="__main__":
    parser=argparse.ArgumentParser(
        prog = 'read_test_data',
        description="数据回收")
    parser.add_argument("--load_csv", help="输入csv文件",type=str,nargs="+",default=[])
    parser.add_argument("--load_maple_txt", help="输入txt文件",type=str,nargs="+",default=[])
    parser.add_argument("--load_maple_dir", help="输入dir",type=str,nargs="+",default=[])
    parser.add_argument("--timeout",help="时间界限, 默认1200s",type=int,default=1200)
    parser.add_argument("--output",help="输出文件名, 默认test_data_lib.csv",type=str,default="data_lib_out.csv")
    arg=parser.parse_args()
    lib=test_data_lib()
    for file_name in arg.load_csv:
        read_csv(lib,file_name)
    for file_name in arg.load_maple_txt:
        read_maple_txt(lib,file_name)
    for file_name in arg.load_maple_dir:
        read_maple_dir(lib,file_name)
    lib.re_unsat()
    lib.virtual_op("maple",10,"cvc5",1190)
    lib.virtual_op("maple",10,"z3",1100)
    
    lib.set_unkown(arg.timeout)
    lib.out_data(arg.output)
    
    polt_Compared(lib,"maple","z3")
    polt_Compared(lib,"maple","cvc5")
    polt_Compared(lib,"maple","yices-smt2")
    
    polt_Compared(lib,"maple","mathsat")
    polt_Compared(lib,"maple-cvc5","cvc5")
    
    polt_line(lib,["maple","z3","cvc5","yices-smt2","mathsat","maple-z3","maple-cvc5"])
    get_table(lib,["maple","z3","cvc5","yices-smt2","mathsat","maple-cvc5"])

    get_compared_table(lib,"maple","cvc5")
    get_compared_table(lib,"maple","z3")
    


# # %%
# print(get_ex_name("/home/ker/Documents/smt-work/QF_NRA/LassoRanker/SV-COMP/LeeJonesBen-Amram-2001POPL-Ex4_true-termination.c_Iteration4_Loop_4-pieceTemplate.smt2"))
# print(get_ex_name('"/home/ker/Projects/local_search_nra/smtlib_parse/result/LassoRanker/SV-COMP/LeeJonesBen-Amram-2001POPL-Ex4_true-termination.c_Iteration4_Loop_4-pieceTemplate.smt2.mpl"'))
# print(get_ex_name('/home/ker/Projects/local_search_nra/smtlib_parse/random_ex_test/random_ex_test2.smt2'))
# print(get_ex_name('random_ex_test/random_ex_test9'))


# # %%
# read_list("/home/ker/Projects/local_search_nra/smtlib_parse/result2/test_list3.csv")
# # %%
# lib=test_data_lib()
# read_csv(lib,"/home/ker/Projects/local_search_nra/smtlib_parse/python/test_data_lib.csv")
# # %%
# lib.get_ex_list()
# # %%
# lib.out_data("/home/ker/Projects/local_search_nra/smtlib_parse/python/test_data_lib3.csv")
# # %%
# lib=test_data_lib()
# read_maple_txt(lib,"/home/ker/Projects/local_search_nra/smtlib_parse/result2/maple_test_1200/maple_test_log_1200_1.txt")
# read_maple_txt(lib,"/home/ker/Projects/local_search_nra/smtlib_parse/result2/maple_test_1200/maple_test_log_1200_2.txt")
# read_maple_txt(lib,"/home/ker/Projects/local_search_nra/smtlib_parse/result2/maple_test_1200/maple_test_log_1200_3.txt")

# # %%
# lib=test_data_lib()
# read_maple_dir(lib,"/home/ker/Projects/local_search_nra/smtlib_parse/result2/maple_test_1200/maple_test")
# # %%

# %%
 #./read_test_data.py --load_csv ../result2/test_data_lib.csv /home/ker/Projects/local_search_nra/smtlib_parse/random_ex_test/random_test_data_lib.csv   --load_maple_txt  ../result2/maple_test_60/maple_test_log_60_1.txt ../result2/maple_test_60/maple_test_log_60_2.txt ../result2/maple_test_60/maple_test_log_60_3.txt  ../result2/maple_test_1200/maple_test_log_1200_1.txt ../result2/maple_test_1200/maple_test_log_1200_2.txt ../result2/maple_test_1200/maple_test_log_1200_3.txt /home/ker/Projects/local_search_nra/smtlib_parse/random_ex_test/maple_test_log2.txt --load_maple_dir ../result2/maple_test_1200/maple_test ../result2/maple_test_60/maple_test
 #./read_test_data.py --load_csv ../result2/test_data_lib.csv    --load_maple_txt  ../result2/maple_test_60/maple_test_log_60_1.txt ../result2/maple_test_60/maple_test_log_60_2.txt ../result2/maple_test_60/maple_test_log_60_3.txt  ../result2/maple_test_1200/maple_test_log_1200_1.txt ../result2/maple_test_1200/maple_test_log_1200_2.txt ../result2/maple_test_1200/maple_test_log_1200_3.txt  --load_maple_dir ../result2/maple_test_1200/maple_test ../result2/maple_test_60/maple_test