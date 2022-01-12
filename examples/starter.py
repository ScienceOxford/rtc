'''
Set up code, do not edit
Adapted from: http://www.multiwingspan.co.uk/micro.php?page=rtc
'''
from microbit import *
import audio

def bcd2dec(bcd):
    return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

def dec2bcd(dec):
    tens, units = divmod(dec, 10)
    return (tens << 4) + units

'''
def set_time(s,m,h,w,dd,mm,yy):
    t = bytes([s,m,h,w,dd,mm,yy-2000])
    for i in range(0,7):
        i2c.write(addr, bytes([i,dec2bcd(t[i])]), repeat=False)
    return
set_time(0,0,10,6,15,1,2022)
'''

def get_time():
    i2c.write(addr, b'\x00', repeat=False)
    buf = i2c.read(addr, 7, repeat=False)
    ss = bcd2dec(buf[0])
    mm = bcd2dec(buf[1])
    if buf[2] & 0x40:
        hh = bcd2dec(buf[2] & 0x1f)
        if buf[2] & 0x20:
            hh += 12
    else:
        hh = bcd2dec(buf[2])
    wday = buf[3]
    DD = bcd2dec(buf[4])
    MM = bcd2dec(buf[5] & 0x1f)
    YY = bcd2dec(buf[6])+2000
    all_time = {'day': str(DD),
                'month': str(MM),
                'year': str(YY),
                'hours': str(hh),
                'minutes': str(mm),
                'seconds': str(ss),
                'weekday': str(wday)}
    print(all_time)
    return (all_time)

addr = 0x68
buf = bytearray(7)









display.show(Image.DUCK)
sleep(1000)
while True:
    if button_a.is_pressed():
        time = get_time()
        display.scroll(time['year'])
    else:
        display.clear()
        sleep(100)
