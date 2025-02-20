path_original="/home/br/Desktop/18.er/außen_wc.gcode"
path_ender="/media/br/AC625/außen_wc.gcode"


homing=True

speed_travel=15000
speed_max=4000
speed_min=600

maße=[150, 101, 18]#x(mm), y(mm), z(mm)
maße_aus_datei=False
umranden_pause=5 #s
umrandung_runden=7
umranden=True


pre_code=["M106 S255", "G4 P500", "M106 S0"]