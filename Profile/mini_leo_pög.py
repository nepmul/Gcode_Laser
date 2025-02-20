#Power: "7.5" Volt
from Profile.default import power_steps

path_original="/home/br/Desktop/Gcode_Laser/Lightburn/Mini_Leo_Pög/mini_leo_pög.gc"
path_ender="/media/br/AC625/kleiner_leo_poeg.gcode"

speed_max=4000
speed_min=450


homing=True



maße=[0, 0, 23.3]#x(mm), y(mm), z(mm) #+7



delay_on=0#1s = 1000
delay_off=0

#only for grayscale
turn_laser_off=False

#power_steps={"220": 400, "50": 1000, "0": 100000} #255-0