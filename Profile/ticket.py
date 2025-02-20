path_original="/home/br/Desktop/18.er/ticket.gc"
path_ender="/media/br/AC625/4_Einladung.gcode"

homing=False

speed_max=350 #350 #35
speed_min=90 #90 #35

maße=[0, 0, 0]#x(mm), y(mm), z(mm)
maße_aus_datei=True
umranden_pause=4 #s
umrandung_runden=3
umranden=True

delay_on=100#1s = 1000
delay_off=0

pre_code=["M106 S255", "G4 P5000", "M106 S0"]
