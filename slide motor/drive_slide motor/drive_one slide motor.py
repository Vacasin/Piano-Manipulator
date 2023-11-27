import RPi.GPIO as GPIO
import time

pinPUL = 18
pinDIR = 24
pinTRAN = 25

def setup():
    GPIO.setmode(GPIO.BCM)
    if GPIO.wiringPiSetupGpio() != 0:
        print("Wiringpi setup failed")
        return False

    GPIO.setup(pinPUL, GPIO.OUT)
    GPIO.setup(pinDIR, GPIO.OUT)
    GPIO.setup(pinTRAN, GPIO.OUT)

    GPIO.output(pinTRAN, GPIO.LOW)

    return True

def LW():
    GPIO.output(pinDIR, GPIO.LOW)

def RW():
    GPIO.output(pinDIR, GPIO.HIGH)

def pulseOnce(delayMicroS):
    GPIO.output(pinPUL, GPIO.HIGH)
    time.sleep(delayMicroS / 1e6)
    GPIO.output(pinPUL, GPIO.LOW)
    time.sleep(delayMicroS / 1e6)

def pulse(count, delayMicroS):
    for _ in range(count):
        pulseOnce(delayMicroS)

def main():
    if not setup():
        return

    LW()
    pulse(1600 * 5, 200)  
    RW()
    pulse(1600 * 5, 200)  

if __name__ == "__main__":
    GPIO.setwarnings(False)  
    GPIO.cleanup()           
    main()
