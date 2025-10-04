#%%
def func_add(fl:list):
    return lambda x:sum(map(lambda a:a(x),fl))
def func_mul(fl:list):
    def f(x):
        tmp=map(lambda a:a(x),fl)
        ans:float=1.0;
        for i in tmp:
            if i:
                ans*=i
            else:
                return 0
        return ans
    return f
def func_sub(fl:list):
    if len(fl)==0:
        return lambda x:0
    elif len(fl)==1:
        return lambda x:-fl[0](x)
    elif len(fl)==2:
        return lambda x:fl[0](x)-fl[1](x)
    else:
        return lambda x:fl[0](x)-func_add(fl[1:])(x)
def func_div(fl:list):
    if len(fl)==0:
        return lambda x:1
    elif len(fl)==1:
        raise  Exception("func_div: 不能只有一个操作符")
    elif len(fl)==2:
        return lambda x:fl[0](x)/fl[1](x)
    else:
        return lambda x:fl[0](x)/func_mul(fl[1:])(x)

def func_l(f1,f2,beta:float=0):
    f=lambda x:f1(x)-f2(x)
    def tmp(x):
        if f(x)<0:
            return 0
        else:
            return f(x)**2+1e-6
    return tmp
def func_le(f1,f2,beta:float=0):
    f=lambda x:f1(x)-f2(x)
    def tmp(x):
        if f(x)<=beta:
            return 0
        else:
            return (f(x)-beta)**2
    return tmp
def func_eq(f1,f2,beta:float=0):
    f=lambda x:f1(x)-f2(x)
    def tmp(x):
        if f(x)<=beta and f(x)>=-beta:
            return 0
        elif f(x)>beta:
            return (f(x)-beta)**2
        else:
            return (f(x)+beta)**2
    return tmp
