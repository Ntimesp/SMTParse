#!/usr/bin/python
from SMTParse.python.runmaple.run_test import test_data_lib
import argparse
def remplname(s:str)->str:
    s=s.replace("/home/ker/Documents/smt-work/QF_NRA/","./result2/")
    s=s.replace(".smt2",".smt2.mpl")
    return s
def resmtname(s:str)->str:
    s=s.replace("./result2/","\"/home/ker/Documents/smt-work/QF_NRA/")
    s=s.replace(".smt2.mpl",".smt2\"")
    return s
def read_mpl(fm)->list[tuple[str,int]]:
    ans:list[tuple[str,int]]=[]
    for i in fm:
        if len(i)>=11 and i[:11]=="namelist:=[":
            i=i[11:]
        if len(i)>0 and i[-1]=="\n":
            i=i[:-1]
        if len(i)>=2 and i[-2:]=="]:":
            i=i[:-2]
        if len(i)>0 and i[-1]==",":
            i=i[:-1]
        
        if len(i):
            tmp=eval(i)
            ans.append((tmp[0],int(tmp[1])))
    return ans;
def read_filelist(fl)->list[tuple[str,int]]:
    ans:list[tuple[str,int]]=[]
    for i in fl:
        tmp=i.split(",")
        ans.append((eval(tmp[0]),int(tmp[1])))
    return ans
def read_csv(file)->test_data_lib:
    ans:test_data_lib=test_data_lib()
    for i in file:
        tmp=i.split(",")
        ans.add_data(tmp[0],tmp[1],tmp[2],float(tmp[3]))
    return ans
def write_mpl(file,tdl:test_data_lib,ls:list[tuple[str,int]])->None:
    file.write("namelist:=[\n")
    for i in ls:
        if i[1]==0:
            name=i[0]
            data=tdl.get_data(resmtname(name))
            ans=set(map(lambda x:data[x][0],data.keys()))
            # print(ans)
            if "unsat" in ans:
                file.write("[\"%s\",%d],\n" % (name,1))
            else:
                file.write("[\"%s\",%d],\n" % (name,0))
                
    file.write("]:")
if __name__=="__main__":
    parser=argparse.ArgumentParser(
        prog = 'csv_to_mpl',
        description="csv_to_mpl")
    
    parser.add_argument("--mplfile",help="输入csv文件名",type=str,required=True)
    parser.add_argument("--filelist",help="输入csv文件名",type=str,required=True)
    parser.add_argument("--csvfile",help="输入csv文件名",type=str,required=True)
    parser.add_argument("--outfile",help="输出mpl文件名",type=str,required=True)
    arg=parser.parse_args()
    lib=None
    mpl_list=None
    flist=None
    fm=open(arg.mplfile,"r");
    fl=open(arg.filelist,"r");
    mpl_list=read_mpl(fm)
    
    flist=read_filelist(fl)
    print(len(mpl_list))
    mpl_list_s:set[str]=set()
    flist_s:set[str]=set()
    
    for i in mpl_list:
        if i[1]==0:
            mpl_list_s.add(i[0])
    for i in flist:
        if i[1]==0:
            flist_s.add(remplname(i[0]))
    
    print(mpl_list_s.symmetric_difference(flist_s),len(mpl_list_s))
    with open(arg.csvfile,"r")as f:
        lib=read_csv(f)
    # print(lib.get_ex_list())
    with open(arg.outfile,"w")as f:
        write_mpl(f,lib,mpl_list)
    
