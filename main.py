## Micropython Default
from machine import Pin, PWM
from time import sleep
import time, random, os

## RPMidi
from rpmidi import RPMidi

# Tick Tock Sound Options

#{
#    key1:{
        
#    key2:value2, ...}
#

analog_click = 0.001
short_digital_beep = 0.005
medium_digital_beep = 0.01
long_digital_beep = 0.05
wtf_digital_beep = 0.1

# Interesting frequency combos
# medium w/ 500
# long w/ 1000

## Setup Pins
## Pins are ordered by top to bottom on both the pico board and buzzers on the perfboard for logical consistency, has no programmatic bearing (I hope lol)
buzzers = [
    PWM(Pin(0)),  # PWM_A[0]
    PWM(Pin(3)),  # PWM_B[1]
    PWM(Pin(6)),  # PWM_A[3]
    PWM(Pin(11)), # PWM_B[5]
    PWM(Pin(15)), # PWM_B[7]
]

buzzer_leds = [
    PWM(Pin(17)),  # PWM_B[0] RED LED w/ 47 Ohm Resistor
    PWM(Pin(18)),  # PWM_A[1] White LED w/ 15 Ohm Resistor
    PWM(Pin(20)),  # PWM_A[2] Blue LED w/ 15 Ohm Resistor
    PWM(Pin(21)),  # PWM_B[2] Yellow LED w/ 47 Ohm Resistor
    PWM(Pin(26))   # PWM_A[5] Green LED w/ 15 Ohm Resistor
]

led_state = [
    0,
    1,
    0,
    1,
    0
]

led = Pin(25, Pin.OUT)

def play_tick():
    for buzzer in buzzers:
        buzzer.duty_u16(1000)
        buzzer.freq(1000) 
    
    sleep(0.001)
    
    for buzzer in buzzers:
        buzzer.duty_u16(0)
        
def toggle_leds():
    led.toggle();
    for i, l in enumerate(buzzer_leds):
        if led_state[i] == 0:
            l.freq(1000)
            l.duty_u16(500)
            led_state[i] = 1
        else:
            l.duty_u16(0)
            led_state[i] = 0
        
def print_time(t):
    hr_12 = t[3] % 12
    if hr_12 == 0:
        hr_12 = 12
        
    period = "AM" if t[3] < 12 else "PM"
    print ("%d/%d/%d %02d:%02d:%02d %s" % (t[1], t[2], t[0], hr_12, t[4], t[5], period), end="\r")

## Blocking call to play midi via RPMidi
def play_midi(song_list):
    midi = RPMidi() # Instantiate RPMidi
    
    # Pick a random midi from list
    #file_name = "/music/" + "umh369.bin"
    file_name = "/music/" + random.choice(song_list)
    print("Playing %s" % file_name)
    f = open(file_name, "rb")
    midi.play_song(f)
    
def generate_song_list():
    song_list = []
    for file in os.listdir("/music"):
        # check only text files
        if file.endswith('.bin'):
            song_list.append(file)
    return song_list
    
## Start Main loop
def main():
    print("Starting Midico Clock...")
    ## Setup Variables
    old_sec = -1
    old_min = -1
    old_hr = -1
    old_day = -1
    
    #Generate list of songs to play
    song_list=generate_song_list()
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
        if hr != old_hr:
            old_hr = hr
            play_midi(song_list)
        if day != old_day:
            old_day = day
            #print("it's a new day!")
            #daily_function()
        sleep(1)
        toggle_leds()

#if __name__ == "__main__":
main()
