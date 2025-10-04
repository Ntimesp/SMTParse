#%%

#%%
class formula:
    def __init__(self,s:str="")->None:
        self.__head:str=s
        self.__ele:list[formula]=[];

    def get_head(self)->str:
        return self.__head;
    
    def get_ele(self)->list:
        return self.__ele;

    
    def __len__(self)->int:
        return len(self.__ele)

    def __getitem__(self,index:int):
        return self.__ele[index];

    def is_int(self)->bool:
        return self.get_head()=="int";

    def is_float(self)->bool:
        return self.get_head()=="float";

    def is_var(self)->bool:
        return self.get_head()=="var";
    
    def is_num(self)->bool:
        return self.is_int() or self.is_float();

    def __str__(self) -> str:
        l:list[str]=[];
        l.append("[")
        l.append(self.__head);
        l.append(" : ");
        l.extend(" , ".join(map(str,self.__ele)))
        l.append(']')
        return "".join(l)
    
    def __repr__(self) -> str:
        return str(self)
    @staticmethod
    def apply(s:str,e:list):
        f=formula(s);
        f.__ele=e;
        return f;

#%%        
class formula_int(formula):
    def __init__(self,a:int)->None:
        super().__init__();
        self.__head:str="int";
        self.__int:int=a;

    def get_head(self)->str:
        return self.__head;
    
    def __int__(self):
        return self.__int;

    def __str__(self) -> str:
        return str(self.__int);

#%%
class formula_float(formula):
    def __init__(self,a:float)->None:
        super().__init__();
        self.__head:str="float";
        self.__float:float=a;

    def get_head(self)->str:
        return self.__head;
    
    def __float__(self):
        return self.__float;

    def __str__(self) -> str:
        return str(self.__float);
#%%

class formula_var(formula):
    def __init__(self,a:str)->None:
        super().__init__();
        self.__head:str="var";
        self.__var:str=a;
    
    def get_head(self)->str:
        return self.__head;
    
    def __str__(self) -> str:
        return self.__var;
#%% 
def apply(s:str,e)->formula:
    return formula.apply(s,e); 

#%% 
def formula_apply_not(f:formula)->formula:
    s=f.get_head()
    k={
        "and":"or",
        "or":"and",
        "<":">=",
        ">=":"<",
        "<=":">",
        ">":"<="
    }
    if s in ["and","or"]:
        l=list(map(formula_apply_not,f.get_ele()))
        # print("l--: ",l,"s--: ",s)
        return apply(k[s],l)
    if s in  ["<","<=",">",">="]:
        return  apply(k[s],f.get_ele())
    if s in ["=","=="]:
        f1=apply("<",f.get_ele());
        f2=apply(">",f.get_ele());
        return apply("or",[f1,f2])
    return f;
