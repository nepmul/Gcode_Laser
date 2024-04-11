path_luban=""
path_ender=""

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
    "",
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

print(file_luban)

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
            new_block.replace("%", " "+parameters)
        file_ender.append(dic_code[code])

        print(f"old:{block} new:{new_block}")

file_ender.append(endcode)

final_file=""
for block in file_ender:
    final_file+=block

with open(path_ender, "w") as f:
    f.write(final_file)







#todo:  "M107 ;laser aus"  ausprobieren

