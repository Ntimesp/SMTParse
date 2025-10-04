#!/usr/bin/python3
#%%
import pexpect
import time
import argparse
#%%
def normout(s:str)->list[str]:
    ans=s.split('\r\n')
    if ans[-1] in ["\r",""]:
        ans.pop()
    return ans
def get_maple(path:str,dir:str="")->pexpect.pty_spawn.spawn:
    MW =path+" -tu"
    if dir!="":
        MW+=" -I "+dir
    print("MW:",MW)
    maple=pexpect.spawn(MW,timeout=None, maxread=200000)
    maple.expect_exact("#-->")
    return maple
def maple_op(maple:pexpect.pty_spawn.spawn,cmd:str)->list[str]:
    if maple.eof():
        return []
    print("cmd",cmd)
    maple.sendline(cmd)
    time.sleep(0.1)
    # maple.sendline("1+1;")
    # while (True):
    if maple.eof():
        return []
    try:
        maple.expect_exact("#-->")
        print(maple.before)
        return normout(maple.before.decode())
    except pexpect.exceptions.EOF:
        # print("maple 终端关闭")
        return normout(maple.before.decode())
        # except:
        #     pass
    print(maple.before)
    return normout(maple.before.decode())

def maple_termin(path:str,dir:str,is_output:bool)->None:
    try:
        maple=get_maple(path,dir)
    except:
        print("maple 进程创建失败")
        return
    file=None
    if is_output:
        fn= time.strftime("maplelog_%Y_%m_%d_%H_%M_%S_")+str(int(time.time()*100)%100)+".log"
        try:
            file=open(fn,"w")
            # maple.logfile=file
        except:
            file=None
            print("log 创建失败")
    while (True):
        if  maple.eof():
            print("maple 终端关闭")
            return
        cmd=input(">");
        ans=maple_op(maple,cmd)
        print(ans)
        print("\n".join(ans[1:]))
        if file:
            file.write(">")
            file.write("\n".join(ans))
            file.write("\n")
            file.flush()
def test_maple(path:str,dir1:str,dir2:str,basicdir:str,outtime:int):
    MW =path+" --echofile=maple_test_log.txt -t"
    print("MW:",MW)
    maple=pexpect.spawn(MW,timeout=None, maxread=200000)
    maple.expect("#-->")
    cmd1="read %s;"% dir1
    print(cmd1)
    # maple.sendline("read %s;"% )
# %%     
if __name__=="__main__":
    parser=argparse.ArgumentParser(
        prog = 'python_maple',
        description="python_maple 交互终端")
    parser.add_argument("path",help="输入maple位置",type=str)
    parser.add_argument("--dir",help="输入包含路径",type=str,default="")
    arg=parser.parse_args()
    maple_termin(arg.path,arg.dir,True)

# ##./python_maple.py /home/ker/maple/maple2020/bin/maple  --dir /home/ker/Projects/local_search_nra

# %%
# path="/home/ker/maple/maple2020/bin/maple"
# MW =path+" -t"
# # %%
# maple=pexpect.spawn(MW)
# # %%
# maple.expect("#-->")
# # %%
# normout(maple.before.decode())
# # %%
# maple.sendline("1+1;")
# # %%
# maple.expect("#-->")
# #%%
# maple.sendline("quit")
# #%%
# maple.before
# #%%
# maple.isalive()
# %%
# maple_termin("/home/ker/maple/maple2020/bin/maple","",False)
# %% 
# maple.getwinsize()