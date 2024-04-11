from tuning import tune

path_luban="luban.nc"
path_ender="ender.gcode"

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
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": ""
}

startcode=[
    "G92 E0 ;reset Extruder",
    "M84 E ;Disable stepper Extruder",
    "G28 ;homing",
    "G1 Z60.00",
    "",
    "",
    ""
]
endcode=[
    "M106 S0 ;Laser aus",
    "G1 Z1500.0"
    "M84 X Y Z E ;Disable all steppers"

]

with open(path_luban, "r") as f:
    file = f.read()

file_luban=file.split("\n")

file_ender=startcode

for block in file_luban:
    code = block.split(" ")[0]

    if block[0]==";": #Kommentare werden nicht mit übertragen
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
            except IndexError: #keine parameter angegeben
                parameters=""
            new_block=new_block.replace("%", " "+parameters)
        file_ender.append(new_block)

        print(f"old:{block} new:{new_block}")

for block in endcode:
    file_ender.append(block)


file_ender=tune(file_ender)
print("\n"*7)

final_file=""
for block in file_ender:
    print(block)
    final_file+=block
    final_file+="\n"

with open(path_ender, "w") as f:
    f.write(final_file)








