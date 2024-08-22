from time import sleep, time
start=time()
from tuning import tune, umrandung_abfahren, find_bounds


from Profile.pög_seriennummer import *

path_original="/home/br/Desktop/Pögs_Seriennummern/lightburn/seriennummer.gcode"
path_ender="/media/br/AC625/seriennummer.gcode"


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

start_vorformatieren=time()
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

print(f"Dauer vorformatieren: {time()-start_vorformatieren}")
full_file=[]

if homing:
    full_file.extend(["G28"])

full_file.extend([f"G1 Z{maße[2]}"])

if umranden:
    full_file.extend(umrandung_abfahren(maße, umrandung_runden, umranden_pause))

start_tune=time()
full_file.extend(tune(file_ender, speed_travel, speed_max, speed_min, delay_on, delay_off))
print(f"Dauer tunign: {time()-start_tune}")

final_file='\n'.join(full_file)
#for block in full_file:
  #  final_file+=block
   # final_file+="\n"

print(final_file)

print(f"Dauer gesammt:{time()-start}")

while True:
    try:
        with open(path_ender, "w") as f:
            f.write(final_file)
        print("Done")
        exit(0)
    except Exception as e:
        print("speicherkarte nicht gefunden", e)
        sleep(4)
