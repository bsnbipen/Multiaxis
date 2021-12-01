
'pump1=device.io.set_all_digital_outputs(1,True)'
'pump2=device.io.set_all_digital_outputs(2,True)'

import re
import math

from zaber_motion.ascii import device
constant_time_velo={"global_1":0,         #time
"global_2":0,                   #time
"global_3":0,                   #time
"global_4":5,                   #time
"global_5":0,                   #time   
"global_6":0,                   #time
"global_7":0,                   #velocity
"global_8":0,                   #velocity
}

constant_pump={"pump_x":0,
"pump_y":0,
"pump_z":0}

intial_dict={"X":0,"Y":0,"Z":0}

class pump():
    def __init__(self,dct_pump):
        self.dct_pump=dct_pump
        self.sum=0
        for key,value in dct_pump.items():
            self.sum+=int(value)


class coord():
    global intial_dict
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
         intial_dict[keys]=self.value_dct[keys]     

    

def output_line(input_file_location,output_file_location):
    init_const=["from zaber_motion import Library\n",
                "from zaber_motion.ascii import AllAxes\n",
                "from zaber_motion.ascii import Device\n",
                "from zaber_motion.ascii import Stream\n",
                "from zaber_motion.ascii import Connection\n",
                "from zaber_motion import Measurement\n",
                "from zaber_motion import Units\n",
                "from PIL import ImageTk, Image\n",
                "Library.enable_device_db_store()\n",
                "with Connection.open_serial_port(\"COM6\") as connection:\n",
                "\tdevice_list = connection.detect_devices()\n",
                "\tdevice = device_list[0]\n",
                "\tnum_streams = device.settings.get('stream.numstreams')\n",
                "\tstream = device.get_stream(1)\n",
                "\tstream.setup_live(2,3,1)\n",
]
    with open (output_file_location,'a') as file:
        file.seek(0) 
        file.truncate()
        for synx in init_const:
            file.write(synx)
    with open(output_file_location,"a") as file:
        with open (input_file_location,'r') as reader:        
            for line_number,line_value in enumerate(reader):
                line_list=line_value.split()
                if (len(line_list)==0):
                    continue
                else:
                        if (re.search(r"\$global\[\d]=",line_list[0])):
                            constant_time_velo["global_"+line_list[0][8]]=line_list[0][11:]
                            print(constant_time_velo)

                
                        elif (re.search(r"\$\D\w\[\d\]\.[A-Z]\=",line_list[0])):
                            constant_pump["pump_"+line_list[0][7]]=line_list[0][9] 
                            if int(constant_pump)==0:
                                file.write("\tpump1=device.io.set_all_digital_outputs(1,False)"+"\n")
                            else:
                                file.write("\tpump1=device.io.set_all_digital_outputs(1,True)"+"\n")
                            val=pump(constant_pump).sum
                            
                            if val==0:
                                file.write("\tstream.wait("+str(constant_time_velo["global_2"])+", Units.TIME_SECONDS)"+"\n")
                                #file.write("\tdevice.all_axes.move_velocity("+str(constant_time_velo["global_7"])+ ", unit = Units.VELOCITY_MILLIMETRES_PER_SECOND)"+"\n")
                                file.write("\tstream.set_max_speed("+str(constant_time_velo["global_7"])+ ", unit = Units.VELOCITY_MILLIMETRES_PER_SECOND)"+"\n")

                            if val==1:
                                #file.write("\tdevice.all_axes.move_velocity("+str(constant_time_velo["global_8"])+ ", unit = Units.VELOCITY_MILLIMETRES_PER_SECOND)"+"\n")
                                file.write("\tstream.set_max_speed("+str(constant_time_velo["global_8"])+ ", unit = Units.VELOCITY_MILLIMETRES_PER_SECOND)"+"\n")
                                file.write("\tstream.wait("+str(constant_time_velo["global_1"])+", unit = Units.TIME_SECONDS)"+"\n")
                            
                        elif (line_list[0]=="G01"):
                            coordinat=coord(line_list)
                            axis={"X":0,"Y":1,"Z":2}
                                #file.write("\taxis_"+axes+".move_absolute("+str(coordinat.default_dict[axes])+", Units.LENGTH_MILLIMETRES, wait_until_idle=False)"+"\n")

                                    #file.write("\tstream.line_absolute_on(["+str(values)+"],[Measurement("+str(100+float(coordinat.default_dict[axes]))+", Units.LENGTH_MILLIMETRES)])\n")
                            file.write("\tstream.line_absolute(Measurement("+str(intial_dict["X"])+", Units.LENGTH_MILLIMETRES),Measurement("+str(intial_dict["Y"])+", Units.LENGTH_MILLIMETRES),Measurement("+str(100+float(intial_dict["Z"]))+", Units.LENGTH_MILLIMETRES))\n")
                            #file.write("\tdevice.all_axes.wait_until_idle()\n")           
output_line(r"C:\Users\bb237\Documents\muliaxis\multiaxis\G-Code\Gcode_example\try_1_cube",r"C:\Users\bb237\Documents\muliaxis\multiaxis\G-Code\Gcode_example\new_file.txt")        #input file location,output file location
        #change the output file location
