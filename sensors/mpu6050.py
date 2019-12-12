#!/usr/bin/python
import smbus
import math

bus = smbus.SMBus(0) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    return (bus.read_byte_data(address, reg) << 8) + bus.read_byte_data(address, reg+1)
 
def read_word_2c(reg):
    val = read_word(reg)
    return ((-((65535 - val) + 1)) if val >= 0x8000 else val)
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    return -math.degrees(math.atan2(x, dist(y,z)))
 
def get_x_rotation(x,y,z):
    return math.degrees(math.atan2(y, dist(x,z)))

def getMpuData():
    # Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)
    
    gyroskop_xout = ("%5d" % read_word_2c(0x43))
    gyroskop_yout = ("%5d" % read_word_2c(0x45))
    gyroskop_zout = ("%5d" % read_word_2c(0x47))
    
    beschleunigung_xout = ("%6d" % read_word_2c(0x3b))
    beschleunigung_yout = ("%6d" % read_word_2c(0x3d))
    beschleunigung_zout = ("%6d" % read_word_2c(0x3f))
    
    beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
    beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
    
    x_rot = get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
    y_rot = get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)

    return [[gyroskop_xout, gyroskop_yout,  gyroskop_zout], [beschleunigung_xout, beschleunigung_yout, beschleunigung_zout], [x_rot, y_rot]]