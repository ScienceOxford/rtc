from microbit import *

# http://www.multiwingspan.co.uk/micro.php?page=rtc

def bcd2dec(bcd):
    return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

def dec2bcd(dec):
    tens, units = divmod(dec, 10)
    return (tens << 4) + units

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
    print(DD, MM, YY, hh, mm, ss, wday)
    return (DD, MM, YY, hh, mm, ss, wday)

addr = 0x68
buf = bytearray(7)

while True:
    if button_a.is_pressed():
        try:
            tm = get_time()
            str_time = '{0:02d}'.format(tm[3]) + ":" + '{0:02d}'.format(tm[4])
            display.scroll(str_time)
        except OSError:
            print("I2C error")
            display.scroll("X")
    elif button_b.is_pressed():
        try:
            tm = get_time()
            str_time = '{0:02d}'.format(tm[0]) + "." + '{0:02d}'.format(tm[1]) + "." + str(tm[2])[-2:]
            display.scroll(str_time)
        except OSError:
            print("I2C error")
            display.scroll("X")
    else:
        display.clear()

# use 'all clocks' to show approx current time
# always show current clock image, unless shaken or button pressed
# add alarm - use speaker to beep, and or LED to flash, when it is a current time
