import re
a="    $DO[8].X=1"
c="    $DO[8].X=0"
b=a.split()
d=c.split()
constant={"global_1":0,         #time
"global_2":0,                   #time
"global_3":0,                   #time
"global_4":5,                   #time
"global_5":0,                   #time   
"global_6":0,                   #time
"global_7":0,                   #velocity
"global_8":0,                   #velocity
}

constant_pump={"pump_X":0,
"pump_Y":0,
"pump_Z":0}

class pump():
    def __init__(self,dct_pump):
        self.dct_pump=dct_pump
        self.sum=0
        for key,value in dct_pump.items():
            self.sum+=int(value)
            


if (re.search(r"\$\D\w\[\d\]\.[A-Z]\=",a)):
    constant_pump["pump_"+b[0][7]]=b[0][9]
    val=pump(constant_pump).sum
    print(val)

if (re.search(r"\$\D\w\[\d\]\.[A-Z]\=",c)):
    constant_pump["pump_"+d[0][7]]=d[0][9]
    val=pump(constant_pump).sum
    print(val)