from microbit import *
import math

def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15:
        return
    if n > 127:
        return
    if value > 127:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)

def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

Start()
lastA = False
lastB = False
lastC = False
wait = False
currentState = 0
last_tilt_x = 0
last_tilt_y = 0
lastVolVal = 0

while True:
    a = button_a.is_pressed()
    b = button_b.is_pressed()
    c = pin1.is_touched()
    if a is True and lastA is False:
        midiControlChange(0, 24, 1)
    if b is True and lastB is False and c is False:
        midiControlChange(0, 25, 1)
    if currentState == 0 and (c is True and lastC is False and wait is False
                              and b is False):
        midiControlChange(0, 27, 1)
        currentState = 1
        wait = True
    if currentState == 1 and (c is True and lastC is False and b is True
                              and wait is False):
        midiControlChange(0, 29, 1)
        currentState = 0
        wait = True
    if currentState == 1 and (c is True and lastC is False and b is False
                              and wait is False):
        midiControlChange(0, 28, 1)
        currentState = 2
        wait = True
    if currentState == 2 and c is True and lastC is False and wait is False:
        midiControlChange(0, 30, 1)
        currentState = 1
        wait = True
    lastA = a
    lastB = b
    lastC = c
    wait = False

    current_tilt_y = accelerometer.get_y()
    if current_tilt_y != last_tilt_y:
        mod_y = math.floor(math.fabs((((current_tilt_y + 1024) / 2048) * 127)))
        midiControlChange(0, 22, mod_y)
        last_tilt_y = current_tilt_y
    sleep(50)

    current_tilt_x = accelerometer.get_x()
    if current_tilt_x != last_tilt_x:
        mod_x = math.floor(math.fabs((((current_tilt_x + 1024) / 2048) * 127)))
        midiControlChange(0, 23, mod_x)
        last_tilt_x = current_tilt_x
    sleep(50)

    currentVolVal = pin2.read_analog()
    if currentVolVal != lastVolVal and ((currentVolVal - lastVolVal > 3)
                                        or (currentVolVal - lastVolVal < -3)):
        mod_vol = math.floor(math.fabs(((currentVolVal / 1018) * 127)))
        midiControlChange(0, 26, mod_vol)
        lastVolVal = currentVolVal
    sleep(50)
