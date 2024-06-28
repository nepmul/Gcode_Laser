from tuning_Lightburn import tune, umrandung_abfahren


path_original="Lightburn/bierathlon24.gc"
path_ender="/media/br/AC625/bierathlon24.gcode"


speed_travel=1500
speed_max=1200
speed_min=40 #kronkorken:5, sonst 60


maße=(20, 20, 3)#xmm, ymm, zmm
umranden=False
umranden_pause=4 #s
umrandung_runden=3


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
if umranden:
    umrandung=umrandung_abfahren(maße, umrandung_runden, umranden_pause)
else:
    umrandung=[]

full_file=umrandung+full_file

final_file=f"G1 Z{maße[2]}"
for block in full_file:
    #print(block)
    final_file+=block
    final_file+="\n"
print(final_file)


with open(path_ender, "w") as f:
    f.write(final_file)
