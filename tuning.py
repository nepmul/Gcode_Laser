def power2speed(speed0, speed100, on_power_threshold, speed_travel, power, power_steps):
    if power <= on_power_threshold:
        return str(speed_travel)+""
    if power_steps !={}:
        for step in power_steps:
            if power >= int(step):
                return power_steps[step]
    dif = speed100-speed0
    return round(power/255*dif+speed0, 2)

def tune(original_gcode, speed_travel, speed_max, speed_min, delay_on, delay_off, turn_laser_off, on_power_threshold, power_steps):
    tuned_gcode=[]
    laser_off_flag=True
    for block in original_gcode:
        new_blocks=[]

        if block=="M106 S0 ":#Laser aus
            if turn_laser_off:
                new_blocks.append(block)
            else:
                pass
            if delay_off != 0:
                new_blocks.append(f"G4 P{delay_off}")
            new_blocks.append(f"G1 F{speed_travel}")
            laser_off_flag=True

        elif block[:4]=="M106":#Laser an
            if laser_off_flag:
                new_blocks.append("M106 S255")
                if delay_on != 0:
                    new_blocks.append(f"G4 P{delay_on}") #1s = 1000
                laser_off_flag=False

            speed=power2speed(speed_max, speed_min, on_power_threshold, speed_travel, float(block[6:]), power_steps)
            new_blocks.append(f"G1 F{speed}")

        else:
            new_blocks.append(block)

        for block in new_blocks:
            tuned_gcode.append(block)
    return tuned_gcode



def find_bounds(code):
    for block in code:
        if block[:9]=="; Bounds:":
            maße=block.split(" ")
            len_x=maße[5][1:]
            len_y=maße[6][1:]

            return float(len_x), float(len_y)

def umrandung_abfahren(maße, runden_abfahren_stk, pause):
    print(maße)
    ränder_abfahren1=[
        f"G0 F3000",
        f"G0 Y{maße[1]}",
        f"G0 X{maße[0]}",
        f"G0 Y0",
        f"G0 X0",
    ]

    neu_positionieren1=[
        f"M18 X Y",
        f"G4 P{pause*1000}",
        f"M300 S440 P200",
        f"G4 P1000",
        f"M17 X Y"
    ]

    umranden=[f"G90"]
    umranden.extend(neu_positionieren1)
    for i in range(runden_abfahren_stk):
        umranden.append(f"M117 noch {runden_abfahren_stk-i} runden")
        umranden.extend(ränder_abfahren1)
        umranden.extend(neu_positionieren1)
    umranden.extend([f"M117 Laser anschalten!", "M300 S440 P200" , f"G4 P5000"])


    #print(ränder_abfahren)
    return umranden



if __name__=="__main__":
    print("\nFalsches Programm du Idiot\n")