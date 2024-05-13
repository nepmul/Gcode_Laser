from tuning import tune, umrandung_abfahren, offset

path_luban="Luban/Strich.nc"
path_ender="Ender_Code.gcode"#"/media/br/AC625/Strich.gcode"

object_height=20
laser_height=5
z_hoop=2

laser_speed=80
travel_speed=5000

umrandung_runden=7

offset_x=30
offset_y=30

laser_height+=object_height
dic_code={ #None=pass, %=nur code ersetzten, ansonsten gesammter block
    "G1": None,
    "G0": None,
    "M106": "",
    "M107": "",
    "G21": "",
    "G90": None,
    "G91": None,
    "M3": "M106%",
    "M5": "M107",
    "": "",
}

startcode=[
    "G92 E0 ;reset Extruder",
    "M84 E ;Disable stepper Extruder",
    "G28 ;homing",
    f"G1 Z{laser_height} F{travel_speed}",
    "",
    ""
]
endcode=[
    "M107",
    f"G1 Z{laser_height+z_hoop*2} F3000",
    "M84 X Y Z E ;Disable all steppers",
    "M106",
    "G4 P500",
    "M106 S0 ;Laser aus",

]

with open(path_luban, "r") as f:
    file = f.read()

file_luban=file.split("\n")

file_ender=[]

for block in file_luban:
    code = block.split(" ")[0]

    if block[0]==";": #Kommentare werden nicht mit übertragen
        pass

    elif "F" in block:
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


file_ender=tune(file_ender,laser_height, z_hoop, laser_speed, travel_speed)
file_ender=offset(file_ender, offset_x, offset_y)

umranden=umrandung_abfahren(file_ender, umrandung_runden)

full_file=startcode

for block in umranden:
    full_file.append(block)

for block in file_ender:
    full_file.append(block)

for block in endcode:
    full_file.append(block)


final_file=""
for block in full_file:
    #print(block)
    final_file+=block
    final_file+="\n"

with open(path_ender, "w") as f:
    f.write(final_file)
