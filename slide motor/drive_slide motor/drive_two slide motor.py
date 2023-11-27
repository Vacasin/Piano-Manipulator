import RPi.GPIO as GPIO
import time

pinPUL = 18
pinDIR = 24
pinTRAN = 23
pinPUL2 = 29
pinDIR2 = 25

a = [0] * 1000
qjl = [0] * 1000
qjr = [0] * 1000
timel = [0.03] * 1000
timer = [0.03] * 1000
stoptimel = [0] * 1000
stoptimer = [0] * 1000

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinPUL, GPIO.OUT)
    GPIO.setup(pinDIR, GPIO.OUT)
    GPIO.setup(pinPUL2, GPIO.OUT)
    GPIO.setup(pinDIR2, GPIO.OUT)
    GPIO.setup(pinTRAN, GPIO.OUT)
    GPIO.output(pinTRAN, GPIO.LOW)
    return True

def LW():
    GPIO.output(pinDIR, GPIO.LOW)

def RW():
    GPIO.output(pinDIR, GPIO.HIGH)

def RW2():
    GPIO.output(pinDIR2, GPIO.LOW)

def LW2():
    GPIO.output(pinDIR2, GPIO.HIGH)

def pulseOnce(delayMicroS):
    GPIO.output(pinPUL, GPIO.HIGH)
    GPIO.output(pinPUL2, GPIO.HIGH)
    time.sleep(delayMicroS / 1e6)
    GPIO.output(pinPUL, GPIO.LOW)
    GPIO.output(pinPUL2, GPIO.LOW)
    time.sleep(delayMicroS / 1e6)

def pulseOnce1(delayMicroS):
    GPIO.output(pinPUL, GPIO.HIGH)
    time.sleep(delayMicroS / 1e6)
    GPIO.output(pinPUL, GPIO.LOW)
    time.sleep(delayMicroS / 1e6)

def pulseOnce2(delayMicroS):
    GPIO.output(pinPUL2, GPIO.HIGH)
    time.sleep(delayMicroS / 1e6)
    GPIO.output(pinPUL2, GPIO.LOW)
    time.sleep(delayMicroS / 1e6)

def pulse(count, delayMicroS, count2, delayMicroS2):
    if count < count2:
        for _ in range(count):
            pulseOnce(delayMicroS)
        for _ in range(count, count2):
            pulseOnce2(delayMicroS2)
    else:
        for _ in range(count2):
            pulseOnce(delayMicroS2)
        for _ in range(count2, count):
            pulseOnce1(delayMicroS)

def main():
    if not setup():
        return

    for i in range(1, 1000):
        a[i] = 0
        qjl[i] = 0
        qjr[i] = 0
        timel[i] = 0.03
        timer[i] = 0.03
        stoptimel = 0
        stoptimer = 0

    with open(file_path, 'r') as file:
    # 使用正则表达式在每一行中找到数字（整数、小数、负数）
    a = [float(match.group()) for line in file for match in re.finditer(r'-?\d+(?:\.\d+)?', line)]
    print(a)

    p = 0
    q = 0
    k = len(a)
    for j in range(0, k, 5):
        if a[j + 2] == 1:
            qjl[p] = a[j]
            timel[p] = a[j + 4]
            stoptimel[p] = a[j + 3]
            p += 1
        if a[j + 2] == -1:
            qjr[q] = a[j]
            timer[q] = a[j + 4]
            stoptimer[p] = a[j + 3]
            q+= 1

    i = 1
    qjl[0] = qjr[0] = 0
    flagl = flagr = 0

    while qjl[i] != 0 or qjr[i] != 0:
        flagl = (qjl[i] - qjl[i - 1]) / 80
        flagr = (qjr[i] - qjr[i - 1]) / 80

        if flagl > 0 and flagr > 0:
            RW()
            LW2()
            pulse(int(1600 * flagl), 6 / timel[i], int(1600 * flagr), 6 / timer[i])
        elif flagl <= 0 and flagr > 0:
            flagl=0-flagl;
            LW()
            LW2()
            pulse(int(1600 * flagl), 6 / timel[i], int(1600 * flagr), 6 / timer[i])
        elif flagl <= 0 and flagr <= 0:
            flagl=0-flagl;
            flagr=0-flagr;
            LW()
            RW2()
            pulse(int(1600 * flagl), 6 / timel[i], int(1600 * flagr), 6 / timer[i])
        else:
            flagr=0-flagr;
            RW()
            RW2()
            pulse(int(1600 * flagl), 6 / timel[i], int(1600 * flagr), 6 / timer[i])
        time.sleep(stoptimel[i])
        i += 1

    flagl = qjl[i - 1] - 0
    flagr = qjr[i - 1] - 0
    LW()
    RW2()
    pulse(int(1600 * flagl), 6 / timel[i], int(1600 * flagr), 6 / timer[i])

if __name__ == "__main__":
    main()
