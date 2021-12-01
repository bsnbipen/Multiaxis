import re
import numpy as np
np.array([1,2,3])
class coord():
    def __init__(self,line_list):
        self.default_dict={"X":None,
        "Y":None,
        "Z":None}

        self.line_list=line_list
        
        for line_values,lines in enumerate(self.line_list):
            if (re.search(r"[A-Z]+\$[a-z]+\D[0-8]+\D",lines)):
             del self.line_list[line_values]
        if (self.line_list[0]=="G01"):
            del self.line_list[0]
        self.value_dct={v:self.line_list[(i+1)] for i,v in enumerate(self.line_list) if v=="X" or v=="Y" or v=="Z"}        #creates a dictionary with X,Y and Z values
        for keys in self.value_dct.keys():
         self.default_dict[keys]=self.value_dct[keys]     


class transformation(coord):
    def __init__(self,line,X_coord=0,Y_coord=0,Z_coord=0):
            self.coord_list=[] 
            transformation_matrix=[[1,0,0,X_coord],[0,1,0,Y_coord],[0,0,1,Z_coord],[0,0,0,1]]
            super.__init__(line)
            for keys,values in self.default_dict.items():
                self.coord_list.append(values)
            self.coord_list.append(1)
            np.array([1,2,3])