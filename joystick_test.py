#!/usr/bin/env
 
import spidev
import os
import subprocess
from subprocess import PIPE
import time

import pyautogui

# Definiere Achsen Channels
# (channel 3 bis 7 koennen für weitere Tasten/Joysticks 
# vergeben werden)
swt_channel = 0
vrx_channel = 1
vry_channel = 2

# Spi oeffnen
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
 
# Funktion zum auslesen des MCP3008
# channel zwischen 0 und 7
def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data

def read():
  # Position bestimmen
  vrx_pos = readChannel(vrx_channel)
  vry_pos = readChannel(vry_channel)
 
  # SW bestimmen
  swt_val = readChannel(swt_channel)
  
  return vrx_pos, vry_pos, swt_val

def open_frozen_bubble():
    count = 0
    p = subprocess.Popen(["frozen-bubble --no-fullscreen --no-timelimit --solo --my-nick 'Willytown'"], stdin=PIPE, shell=True)

def main():
    open_frozen_bubble()
    print("letsgo")
    
    direction = 'l'
    while True:
        x, y, z = read()
        
        if x > 550:
            pyautogui.keyDown('left')
        else:
            pyautogui.keyUp('left')
        
        if x < 500:
            pyautogui.keyDown('right')
        else:
            pyautogui.keyUp('right')
        
        if z < 2:
            pyautogui.keyDown('up')
        else:
            pyautogui.keyUp('up')
        
        print(x, y, z)
        time.sleep(0.02)
        

if __name__ == "__main__":
    main()
#main()

