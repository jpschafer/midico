## Micropython Default
from machine import Pin
from time import sleep
import time

## RPMidi
from rpmidi import RPMidi
from songs import SongData

## Setup Pins
led = Pin(25, Pin.OUT)

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
    songs = SongData() # Load songs. See songs.py
    midi.play_song(songs.morning_music()) # Konami Bubble System "Morning Musi
    
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