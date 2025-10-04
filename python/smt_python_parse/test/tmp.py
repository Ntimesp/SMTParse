#%%
s="[and : [and : [and : [and : [and : [and : [and : [> : [+ : x0 , [* : x1 , x2]] , [+ : x4 , [* : x5 , x2]]] , [>= : [+ : x0 , [* : x1 , x2]] , [+ : x4 , [* : x5 , x2]]]] , [>= : [* : x1 , x3] , [* : x5 , x3]]] , [and : [and : [> : [+ : x0 , [* : x1 , x2]] , [+ : x0 , [* : x1 , [+ : x6 , [* : x7 , x2]]]]] , [>= : [+ : x0 , [* : x1 , x2]] , [+ : x0 , [* : x1 , [+ : x6 , [* : x7 , x2]]]]]] , [>= : [* : x1 , x3] , [* : x1 , [* : x7 , x3]]]]] , [and : [and : [> : [+ : x6 , [* : x7 , x2]] , 0] , [>= : [+ : x6 , [* : x7 , x2]] , 0]] , [>= : [* : x7 , x3] , 1]]] , [and : [> : [+ : x8 , [* : x9 , x10]] , [+ : x2 , [* : x3 , x10]]] , [>= : [+ : x8 , [* : x9 , x10]] , [+ : x2 , [* : x3 , x10]]]]] , [and : [and : [> : [+ : x8 , [* : x9 , x2]] , [+ : [+ : x11 , [* : x12 , x2]] , [* : x13 , [+ : x8 , [* : x9 , [+ : x6 , [* : x7 , x2]]]]]]] , [>= : [+ : x8 , [* : x9 , x2]] , [+ : [+ : x11 , [* : x12 , x2]] , [* : x13 , [+ : x8 , [* : x9 , [+ : x6 , [* : x7 , x2]]]]]]]] , [>= : [* : x9 , x3] , [+ : [* : x12 , x3] , [* : x13 , [* : x9 , [* : x7 , x3]]]]]]] , [and : [and : [and : [> : [+ : x0 , [* : x1 , x2]] , [+ : x4 , [* : x5 , x2]]] , [>= : [+ : x0 , [* : x1 , x2]] , [+ : x4 , [* : x5 , x2]]]] , [>= : [* : x1 , x3] , [* : x5 , x3]]] , [and : [and : [> : [+ : x0 , [* : x1 , x2]] , [+ : x0 , [* : x1 , [+ : x6 , [* : x7 , x2]]]]] , [>= : [+ : x0 , [* : x1 , x2]] , [+ : x0 , [* : x1 , [+ : x6 , [* : x7 , x2]]]]]] , [>= : [* : x1 , x3] , [* : x1 , [* : x7 , x3]]]]]]"
stack=0
index=0
s_list=[]
tmp_str=''
while True:
    # print("time: ",time)
    if s[index]=='[':
        time=stack
        stack+=1
        while not time==0:
            tmp_str+="    "
            time-=1
        tmp_str+='['
        # tmp_str+='\n'
        s_list.append(tmp_str)
        index+=1
    elif s[index]==']':
        stack-=1
        time=stack
        while not time==0:
            tmp_str+="    "
            time-=1
        tmp_str+=']'
        # tmp_str+='\n'
        s_list.append(tmp_str)
        index+=1
    else:
        time=stack
        while not time==0:
            tmp_str+="    "
            time-=1
        while not s[index] in ['[',']']:
            # print("not kuohao: ", tmp_str)
            tmp_str+=s[index]
            index+=1
            if index>=len(s):
                break
        # tmp_str+='\n'
        s_list.append(tmp_str)
        # stack+=1
    tmp_str=""
    if stack==0:
        break
# print(s_list)
for each_str in s_list:
    print(each_str)
# %%
