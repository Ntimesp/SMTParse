#!/usr/bin/python3
import os
import time
import argparse
import multiprocessing
import time
class test_data_lib:
    def __init__(self) -> None:
        self.__data:dict[str,dict[str,tuple[str,float]]]=dict()
        # self.__lock=multiprocessing.Lock()
    def get_ex_list(self)->list[str]:
        return self.__data.keys()
    def add_data_com(self,ex_name:str,op:str,ans:str,t:float)->None:
        if not(ex_name in self.__data):
            self.__data[ex_name]=dict()
        if not(op in self.__data[ex_name]) or (self.__data[ex_name][op][0]=="unknown" and ans!="unknown"):
            self.__data[ex_name][op]=(ans,t)
        if ans=="unknown":
            return
        assert(ans==self.__data[ex_name][op][0])
        if t<self.__data[ex_name][op][1]:
            self.__data[ex_name][op]=(ans,t)
            
    def add_data(self,ex_name:str,op:str,ans:str,t:float)->None:
        # with self.__lock:
        # print("add_data %s %s %s %f start" % (ex_name,op,ans,t))
        if not(ex_name in self.__data):
            self.__data[ex_name]=dict()
        self.__data[ex_name][op]=(ans,t)
        # print("add_data %s %s %s %f down" % (ex_name,op,ans,t))
    def get_data(self,ex_name:str,op:str|None=None)->dict[str,tuple[str,float]]|tuple[str,float]:
        # with self.__lock:
        if not(ex_name in self.__data):
            self.__data[ex_name]=dict()
        if op==None:
            return self.__data[ex_name]
        if not(op in self.__data[ex_name]):
            return "None",-1;
        return self.__data[ex_name][op]
    def out_data(self,filename:str)->None:
        f=open(filename,"w")
        for ex in self.__data:
            for op in self.__data[ex]:
                # print(ex,op)
                tmp:list[str]=[ex,op,self.__data[ex][op][0],str(self.__data[ex][op][1])]
                f.write(",".join(tmp));
                f.write("\n");
        f.close()
    def re_unsat(self)->None:
        l=[];
        for i in self.__data:
            for op in self.__data[i]:
                if  self.__data[i][op][0]=="unsat":
                    l.append(i)
                    break
        for i in l:
            self.__data.pop(i)
    def set_unkown(self,t,op_l=None)->None:
        for i in self.__data:
            ol=self.__data[i].keys()
            if op_l!=None:
                op=op_l
            for op in ol:
                if  self.__data[i][op][0]=="unknown":
                    self.__data[i][op]=("unknown",t)
    def virtual_op(self,op1,t1,op2,t2):
        nop=f'{op1}-{op2}'
        for i in self.__data:
            if self.__data[i][op1][0]in ["sat","unsat"] and self.__data[i][op1][1]<=t1:
                self.__data[i][nop]=self.__data[i][op1];
            elif self.__data[i][op2][0]in ["sat","unsat"] and self.__data[i][op2][1]<=t2:
                self.__data[i][nop]=(self.__data[i][op2][0],self.__data[i][op2][1]+t1);
            else:
                self.__data[i][nop]=("unknown",-1);
                
        
def test(op:str,file:str,t:int)->tuple[str,float]:
    T:float=time.time();
    print("test",file, op)
    x:str=""
    x=os.popen("timeout "+str(t)+"s "+op+" "+file).read().lower()
    T=time.time()-T;
    # print("test",file,x)
    ans:str="unknown";
    if (x.find("unsat")>=0):
        ans="unsat"
    elif (x.find("sat")>=0):
        ans="sat"
    print(file,op,ans,T)
    return ans,T

def print_error (value):
    print(value)
def test_and_save(file:str,op:str,outtime:int,lst,q):
    # print("test_and_save %s %s" % (op,file))
    ans,t=test(op,file,outtime)
    # with lst.get_lock():
    lst.append((file,op,ans,t))
    # with lock:
    q.put((file,op,ans,t))
def print_log(q):
    fn= time.strftime("log_%Y_%m_%d_%H_%M_%S_")+str(int(time.time()*100)%100)+".log"
    with open(fn, 'w') as f:
        while 1:
            m = q.get()
            if m == 'end':
                f.write('end\n')
                break
            f.write(str(m) + '\n')
            f.flush()

            
def run_test(fl:list[str],sl:list[str],outtime:int=1200,pool_num:int=1,load_data:dict[tuple[str,str],tuple[str,str,str,float]]=dict())->test_data_lib:
    result=test_data_lib();
    print("pool_num=",pool_num)
    pool=multiprocessing.Pool(processes=pool_num)
    lst=multiprocessing.Manager().list()
    q=multiprocessing.Manager().Queue()
    # lock=multiprocessing.Manager().Lock()
    print("run_test start")
    # l:list[tuple[str,str]]=[]
    watcher = pool.apply_async(print_log, (q,))
    jobs = []
    for ex_name in fl:
        for op in sl:
            # print("run_test add %s %s" % (ex_name,op))        
            # l.append((ex_name,op));
            if (ex_name,op) in load_data:
                q.put(load_data[(ex_name,op)])
                lst.append(load_data[(ex_name,op)])
            else:
                job=pool.apply_async(func=test_and_save,args=(ex_name,op,outtime,lst,q,),error_callback=print_error)
                jobs.append(job)
            # pool.map(lambda x:)
            # ans,t=test(op,ex_name,outtime)
            # result.add_data(ex_name,op,ans,t);
    for job in jobs: 
        job.get()
    q.put('end')
    pool.close()
    pool.join()
    for i in lst:
        result.add_data(i[0],i[1],i[2],i[3])
    print("run_test end") 
    return result;
def get_filetest(csv_file:str)->list[str]:
    ans:list[str]=[]
    with open(csv_file) as f:
        for line in f:
            tmp=line.split(",")
            assert len(tmp)==2,"csv 格式不对"
            try:
                b=int(tmp[1])
            except:
                raise Exception("csv 格式不对")
            if b==0:
                ans.append(tmp[0])
    return ans

if __name__=="__main__":
    parser=argparse.ArgumentParser(
        prog = 'run_test',
        description="smt2 测试脚本")
    group1= parser.add_mutually_exclusive_group(required=True)
    group1.add_argument("--ex_list",help="输入例子列表",nargs="+",type=str,default=[])
    group1.add_argument("--csv",help="输入例子列表的csv文件 ",type=str,default="")
    parser.add_argument("op_list",help="输入测试求解器列表",nargs="+",type=str)
    parser.add_argument("--timeout",help="时间界限, 默认1200s",type=int,default=1200)
    parser.add_argument("--output",help="输出文件名, 默认test_data_lib.csv",type=str,default="test_data_lib.csv")
    parser.add_argument("--pools",help="并发数目, 默认1",type=int,default=1)
    parser.add_argument("--load_log", help="输入log文件",type=str,default="")
    parser.add_argument("--load_csv", help="输入csv文件",type=str,default="")
    
    arg=parser.parse_args()
    filelist=arg.ex_list
    if arg.csv:
        filelist=get_filetest(arg.csv)
    oplist=arg.op_list
    timeout=arg.timeout
    print("filelist_len:",len(filelist))
    print("oplist:",oplist)
    print("timeout:",timeout)
    print("pools_num:",arg.pools)
    
    load_data:dict[tuple[str,str],tuple[str,str,str,float]]=dict()
    if arg.load_log!="":
        with open(arg.load_log,"r") as f:
            for line in f:
                if line=="end\n":
                    break;
                # print(line)
                tmp=eval(line)
                assert(type(tmp)==tuple and type(tmp[0])==str and type(tmp[1])==str and type(tmp[2])==str and type(tmp[3])==float)
                load_data[(tmp[0],tmp[1])]=tmp
    if arg.load_csv!="":
        with open(arg.load_csv,"r") as f:
            for line in f:
                # print(line)
                tmp=line.split(",")
                tmp[3]=float(tmp[3])
                assert(type(tmp)==list and type(tmp[0])==str and type(tmp[1])==str and type(tmp[2])==str and type(tmp[3])==float)
                load_data[(tmp[0],tmp[1])]=tmp

    testdatalib=run_test(filelist,oplist,timeout,arg.pools,load_data)
    testdatalib.out_data(arg.output)

    
# ./run_test.py --csv ../result/file_list.csv z3 cvc5 yices-smt2 mathsat --output test_data_lib.csv  --timeout 1200 --pools 16 --load_log log_2023_01_16_02_08_00_79.log