from tuning_Lightburn import tune, umrandung_abfahren


path_original="Lightburn/stammeslogo_minipoeg.nc"
path_ender="/media/br/AC625/stammeslogo_22mm.gcode"

umrandung_runden=3

speed_travel=1500
speed_max=1200
speed_min=60 #kronkorken:5


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


with open(path_original, "r") as f:
    file = f.read()

file_original=file.split("\n")

file_ender=[]
for block in file_original:

    if "F" in block: #alle geschwindigkeiten von Ligtburn raus filtern
        block=block.split("F")[0]

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
        file_ender.append(dic_code[code])

full_file=tune(file_ender, speed_travel, speed_max, speed_min)

final_file=""
for block in full_file:
    print(block)
    final_file+=block
    final_file+="\n"


#umrandung_abfahren(full_file, umrandung_runden)





with open(path_ender, "w") as f:
    f.write(final_file)
