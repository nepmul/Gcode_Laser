
def power2speed(speed0, speed100, power):
    dif = speed100-speed0
    return round(power/255*dif+speed0, 2)

def tune(original_gcode, speed_travel, speed_max, speed_min):
    tuned_gcode=[]
    laser_off_flag=True
    for block in original_gcode:
        new_blocks=[]

        if block=="M106 S0 ":#Laser aus
            new_blocks.append(block)
            new_blocks.append("G4 P100")
            new_blocks.append(f"G1 F{speed_travel}")
            laser_off_flag=True

        elif block[:4]=="M106":#Laser an
            if laser_off_flag:
                new_blocks.append("M106 S255")
                new_blocks.append("G4 P50") #1s = 1000
                laser_off_flag=False

            speed=power2speed(speed_max, speed_min, float(block[6:]))
            new_blocks.append(f"G1 F{speed}")

        else:
            new_blocks.append(block)

        for block in new_blocks:
            tuned_gcode.append(block)
    return tuned_gcode


def umrandung_abfahren(gcode, runden_abfahren):
    x_max=-1000
    x_min=1000
    y_max=-1000
    y_min=1000
    for block in gcode:
        print(block)
        parts_block=block.split(" ")
        if parts_block[0] == "G1" and parts_block[1][0]=="X":
                part=parts_block[1]
                xy=part[1:].split("Y")
                print(xy)
                value=float(xy[0])
                if value > x_max:
                    x_max=value
                if value < x_min:
                    x_min=value

                try:
                    value=float(xy[1])
                    print("------------------------", value)

                    if value > y_max:
                        y_max=value
                    if value < y_min:
                        y_min=value
                except IndexError:
                    pass

    print(x_max)
    print(x_min)
    print(y_max)
    print(y_min)

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


