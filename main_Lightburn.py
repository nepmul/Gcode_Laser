from tuning_Lightburn import tune, umrandung_abfahren, find_bounds


path_original="Lightburn/geb_bente.gc"
path_ender="/media/br/AC625/geb_bente.gcode"

homing=False

speed_travel=1500
speed_max=1200
speed_min=200#edding500


maße=[0, 0, 0]#x(mm), y(mm), z(mm)
maße_aus_datei=True
umranden_pause=5 #s
umrandung_runden=6
umranden=True


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

if maße_aus_datei:
    maße[0], maße[1]=find_bounds(file_original)
print(f"Ausgelesene Maße:{maße}\n")


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


full_file=[]

if homing:
    full_file.extend(["G28"])

full_file.extend([f"G1 Z{maße[2]}"])

if umranden:
    full_file.extend(umrandung_abfahren(maße, umrandung_runden, umranden_pause))

full_file.extend(tune(file_ender, speed_travel, speed_max, speed_min))

final_file=f""
for block in full_file:
    final_file+=block
    final_file+="\n"
print(final_file)


with open(path_ender, "w") as f:
    f.write(final_file)
