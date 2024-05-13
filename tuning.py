

def tune(original_gcode, laser_height, z_hoop, laser_speed, travel_speed):
    tuned_gcode=[]
    for block in original_gcode:
        new_blocks=[block]

        if block=="M106":#Laser an
            new_blocks.insert(0, f"G0 Z{laser_height}")
            new_blocks.insert(1, f"G1 F{laser_speed}")
            new_blocks.append("G4 P120") #1s = 1000

        elif block=="M107":#Laser aus
            new_blocks.append(f"G1 F{travel_speed}")
            new_blocks.append(f"G0 Z{laser_height+z_hoop}")
            new_blocks.append("G4 P200")

        #elif block.split(" ")[0] == "G0":
         #   new_blocks.insert(0, f"G0 {travel_speed}")
          #  new_blocks.append(f"G1 {laser_speed}")

        for block in new_blocks:
            tuned_gcode.append(block)

    return tuned_gcode


def umrandung_abfahren(gcode, runden_abfahren):
    x_max=0
    x_min=1000
    y_max=0
    y_min=1000
    for block in gcode:
        parts_block=block.split(" ")
        if parts_block[0] == "G1" or parts_block[0] == "G0":
            for part in parts_block:
                value=float(part[1:])

                if part[0]=="X":
                    if value > x_max:
                        x_max=value
                    if value < x_min:
                        x_min=value

                if part[0]=="Y":
                    if value > y_max:
                        y_max=value
                    if value < y_min:
                        y_min=value

    #print(x_max)
    #print(x_min)
    #print(y_max)
    #print(y_min)

    print(f"Objektgroße: {round(x_max-x_min, 1)} * {round(y_max-y_min, 2)}")
    ränder_abfahren1=[
        f"G0 X{x_min} Y{y_min} F5000",
        f"G0 Y{y_max}",
        f"G0 X{x_max}",
        f"G0 Y{y_min}",
        f"G0 X{x_min} Y{y_min}",
        f"G4 P4000"# sek warten
    ]

    ränder_abfahren=[]
    for i in range(runden_abfahren):
        for block in ränder_abfahren1:
            ränder_abfahren.append(block)

    #print(ränder_abfahren)
    return ränder_abfahren


def offset(gcode, offset_x, offset_y):
    new_gcode=[]
    for block in gcode:
        print(block)
        args=block.split(" ")
        if not args == [""]:


            for arg in args:
                if arg[0] == "X":
                    new_arg = "X"+str(round(float(arg[1:]) + offset_x, 2))#offset wird auf gegebenen wert drauf gerechnet
                    block=block.replace(arg, new_arg)
                elif arg[0] == "Y":
                    new_arg = "Y"+str(round(float(arg[1:]) + offset_y, 2))
                    block=block.replace(arg, new_arg)


        print(block)
        new_gcode.append(block)

    return new_gcode