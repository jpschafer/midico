## Micropython Default
from machine import Pin, PWM
from time import sleep
import time

## RPMidi
from rpmidi import RPMidi
from songs import SongData

# Tick Tock Sound Options

#{
#    key1:{
        
#    key2:value2, ...}
#

analog_click = 0.001
short_digital_beep = 0.005
medium_digital_beep = 0.001
long_digital_beep = 0.05
wtf_digital_beep = 0.1

# Interesting frequency combos
# medium w/ 500
# long w/ 1000

## Setup Pins
buzzers = [
    PWM(Pin(16)),
    PWM(Pin(17)),
    PWM(Pin(18)),
    PWM(Pin(19)),
    PWM(Pin(20))
]

led = Pin(25, Pin.OUT)

def play_tick():
    for buzzer in buzzers:
        buzzer.duty_u16(1000)
        buzzer.freq(1000)
    
    sleep(analog_click)
    
    for buzzer in buzzers:
        buzzer.duty_u16(0)
def print_time(t):
    hr_12 = t[3] % 12
    if hr_12 == 0:
        hr_12 = 12
        
    period = "AM" if t[3] < 12 else "PM"
    print ("%d/%d/%d %02d:%02d:%02d %s" % (t[1], t[2], t[0], hr_12, t[4], t[5], period), end="\r")

## Blocking call to play midi via RPMidi
def play_midi():
    print("Playing midi...")
    midi = RPMidi() # Instantiate RPMidi
    
    f = open("enigmatic_encounter_edited.bin", "rb")
    midi.play_song(f)
    #songs = SongData() # Load songs. See songs.py
    #midi.play_song(songs.enigmatic_encounter()) # Konami Bubble System "Morning Musi
    
## Start Main loop
def main():
    print("Starting Midico Clock...")
    ## Setup Variables
    old_sec = -1
    old_min = -1
    old_hr = -1
    old_day = -1
    
    ## Loop
    while True:
        t = time.localtime()
        
        sec = t[5]
        min = t[4]
        hr = t[3]
        day = t[2]
        
        if sec != old_sec:
            old_sec = sec
            play_tick()
            print_time(t)
        if min != old_min:
            old_min = min
            #print("min updated")
        if hr != old_hr:
            old_hr = hr
            play_midi()
        if day != old_day:
            old_day = day
            #print("it's a new day!")
            #daily_function()
        sleep(1)
        led.toggle()

if __name__ == "__main__":
    main()