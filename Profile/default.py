path_original="/home/br/Desktop/Gcode_Laser/Lightburn/laser_projekt.gcode"
path_ender="/media/br/AC625/laser_projekt.gcode"


homing=False

speed_travel=100000
speed_max=4000
speed_min=200

maße=[0, 0, 0]#x(mm), y(mm), z(mm)
maße_aus_datei=False
umranden_pause=5 #s
umrandung_runden=5
umranden=False

delay_on=80#1s = 1000
delay_off=100

turn_laser_off=True

on_power_threshold=0 #0-255 everything below this value is driven with travel_speed

pre_code=[]

power_steps={} #example:{"200": 150, "50": 400, "0": 15000} #255-0 #255 bis 200 mit 150mm/s,...
