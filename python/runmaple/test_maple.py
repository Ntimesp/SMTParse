#!/usr/bin/python3
#%%
import pexpect
import time
import argparse
import os
import re
#%%
def re_ansi(data):
    ansi_escape = re.compile(rb'\x1B[@-_][0-?]*[ -/]*[@-~]')
    data = ansi_escape.sub(b'', data)
    return data
def test_maple(path:str,log_file,dir1:str,dir2:str,outtime:int,start:int=0,end:int=-1):
    with open(dir2,"r") as f:
        lst=f.read().split("\n")
        if end<0:
            end=len(lst)
        for i in range(start,end):#
            ex_name,index=lst[i].split(",")
            index=int(index)
            print(ex_name,index)
            if index!=0:
                continue
            tmp=time.time()
            print(time.strftime(f"++ start {i}:%Y_%m_%d_%H_%M_%S"))
            log_file.write(time.strftime(f"++ start {i}:%Y_%m_%d_%H_%M_%S\n"))
            log_file.write(ex_name)
            log_file.write("\n")
            MW_tmp=f"maple_test/sub_{dir2.split('/')[-1]}_{outtime}_{i}.log"
            MW =path+" --echofile=%s -t" % MW_tmp
            print("MW:",MW)
            try:
                with pexpect.spawn(MW,timeout=outtime+10, maxread=200000) as maple:
                
                    maple.expect("#-->")
                    cmd1="read \"%s\";"% dir1
                    print(cmd1)
                    maple.sendline(cmd1)
                    # cmd2="read \"%s\";"% dir2
                    # print(cmd2)
                    # maple.sendline(cmd2)
                    cmd3=f"NRA_solve({ex_name}, prep=-1,outtime={outtime}); " 
                    print(cmd3)
                    maple.sendline(cmd3)
                    cmd4="quit;"
                    print(cmd4)
                    maple.sendline(cmd4)
                    maple.expect(pexpect.EOF)
                    ss=re_ansi(maple.before).decode()
                    print(ss)
                    log_file.write(ss)
                    log_file.write("\n")
            except:
                log_file.write("+ maple 故障\n")
                print("+ maple 故障\n")
            print(f"all time:{time.time()-tmp}")
            log_file.write(f"++ all time:{time.time()-tmp}\n")
            log_file.flush()
        
        
# %%     
if __name__=="__main__":
    parser=argparse.ArgumentParser(
        prog = 'test_maple',
        description="maple 测试脚本")
    parser.add_argument("path",help="输入maple位置",type=str)
    parser.add_argument("dir1",help="输入程序位置",type=str)
    parser.add_argument("dir2",help="输入测试列表位置",type=str)
    tmp=time.strftime("maple_test_log_%Y_%m_%d_%H_%M_%S.log")
    parser.add_argument("--log_file",help="输入log_file， 默认%s" % tmp,type=str,default=tmp)
    
    # parser.add_argument("--basicdir",help="输入basicdir， 默认空",type=str,default="")
    parser.add_argument("--outtime",help="输入outtime， 默认1200",type=int,default=1200)
    parser.add_argument("--start",help="输入start index， 默认0",type=int,default=0)
    parser.add_argument("--end",help="输入start index， 默认0",type=int,default=-1)
    
    arg=parser.parse_args()
    
    # cmd=f'{arg.path} --echofile={arg.log_file} -t -i {arg.dir1}  -i {arg.dir2} -c "NRA_solve_test(namelist, basicdir=basicdir_str,outtime={arg.outtime});"'
    # print(cmd)
    # print("nohup %s > runoob1.log 2>&1 &" % cmd)
    
    # os.popen(cmd)
    with open(arg.log_file,"w") as f:
        test_maple(arg.path,f,arg.dir1,arg.dir2,arg.outtime,arg.start,arg.end)
# ../python/test_maple.py /home/ker/maple/maple2022/bin/maple "/home/ker/Projects/local_search_nra/code/local_search_v14_new.mpl" "/home/ker/Projects/local_search_nra/smtlib_parse/result2/test_list3.csv" --timeout 1200
# 1526848 1527755  1528672 1528941