sections=10#stk
section_width=7#mm
height=10#mm
spacing=0.1#mm

min_speed=200
max_speed=800

travel_speed=3000

delay_on=100 #1000=1s
delay_off=100 #1000=1s
overdrawing=10#mm

laser_on=["M106 S255", f"G4 P{delay_on}"]
laser_off=["M106 S0"]#, f"G4 P{delay_off}"]

startcode=[f"G91", f"M117 {min_speed} - {max_speed}; {sections} * {section_width}mm"]

full_widt=section_width*sections#mm
speed_dif=max_speed-min_speed
speed_change_per_section=speed_dif/(sections-1)

laser_height=0#mm


line=[] #markierungen für abschnitte
section_marker=[]
section_marker.append(f"G1 X{section_width}")
section_marker.extend(laser_on)
section_marker.append(f"G4 P300")
section_marker.extend(laser_off)
for i in range(sections):
    line.extend(section_marker)
line.append(f"G1 X-{full_widt} Y{spacing} F{travel_speed}")
for i in range(4):
    startcode.extend(line)
    laser_height+=spacing


line=[]#linie unter teststrecke
line.extend(laser_on)
line.append(f"G1 X{full_widt} F{min_speed}")
line.extend(laser_off)
line.append(f"G1 X-{full_widt} Y{spacing} F{travel_speed}")
for i in range(3):
    laser_height+=spacing
    startcode.extend(line)


line=laser_on#eigentliche teststrecke
for i in range(sections):
    speed=round(min_speed+i*speed_change_per_section, 2)
    #line.append(f"M117 {speed}")
    line.append(f"G1 X{section_width} F{speed}")
line.extend(laser_off)
line.append(f"G1 X{overdrawing}")
line.append(f"G1 X-{full_widt+overdrawing} Y{spacing} F{travel_speed}")

gcode=startcode
while laser_height+spacing <= height:
    laser_height+=spacing
    gcode.extend(line)

del gcode[-1]

gcode.append(f"G4 P10000")

file=""
print(gcode)
for i in gcode:
    file+=i+"\n"
    print(i)

#hübsche anzeige am Ende
result="\n"*5
for i in range(sections):
    result+=f"|{i+1}:   "
    result+=str(round(min_speed+i*speed_change_per_section, 2))
    result+="     |"
result+="\n"*3
file+=result
print(result)


with open("/media/br/AC625/gray-speed_calibration.gcode", "w") as f:
    f.write(file)

