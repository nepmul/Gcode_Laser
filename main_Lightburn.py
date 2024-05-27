path_original="Lightburn/Leo_muster_ausschnitt_grayscale.nc"
path_ender="/media/br/AC625/grayscale.gcode"

umrandung_runden=3

speed_travel=300
speed_max=200
speed_min=100


dic_code={ #None=pass, %=nur code ersetzten, ansonsten gesammter block
    "G28": None,
    "G1": None,
    "G0": None,
    "G21": "",
    "G90": None,
    "G91": None,
    "G4": None,
    "M106": None,
    "M8": "",
    "M9": ""
}


def power2speed(speed0, speed100, power):
    dif = speed100-speed0
    return round(power/255*dif+speed0, 2)

def tune(original_gcode):
    tuned_gcode=[]
    laser_off_flag=True
    for block in original_gcode:
        new_blocks=[]

        if block=="M106 S0 ":#Laser aus
            new_blocks.append(block)
            new_blocks.append("G4 P200")
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
        """
        elif block=="G90":
            new_blocks.append("G1 X60 Y50")
        """
        for block in new_blocks:
            tuned_gcode.append(block)
    return tuned_gcode

with open(path_original, "r") as f:
    file = f.read()

file_original=file.split("\n")

file_ender=[]
for block in file_original:
    code = block.split(" ")[0]
    if block=="":
        pass
    elif block[0]==";": #Kommentare und Leerzeilen werden nicht mit übertragen
        pass


    elif code not in dic_code:
        print(f"Unbekannter gcode befehl!\n{code}")
        quit(1)

    elif dic_code[code] == None:
        file_ender.append(block)

    else:
        new_block=dic_code[code]
        if "%" in new_block:
            try:
                parameters=block.split(" ", 1)[1]#alles außer dem code
                new_block=new_block.replace("%", " "+parameters)
            except IndexError: #keine parameter angegeben
                new_block=new_block.replace("%", "")

        file_ender.append(new_block)

full_file=tune(file_ender)

final_file=""
for block in full_file:
    print(block)
    final_file+=block
    final_file+="\n"

with open(path_ender, "w") as f:
    f.write(final_file)
    print(final_file)