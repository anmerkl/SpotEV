import mraa
import time

import os

TRIG = mraa.Gpio(11)
ECHO = mraa.Gpio(10)
TRIG2 = mraa.Gpio(6)
ECHO2 = mraa.Gpio(5)

TRIG.dir(mraa.DIR_OUT)
ECHO.dir(mraa.DIR_IN)
TRIG2.dir(mraa.DIR_OUT)
ECHO2.dir(mraa.DIR_IN)

NUM_SAMPLES = 200
SUCCESS_PERCENT = 0.60
countOne = 0
countTwo = 0
carOneTime = 0
carTwoTime = 0


def poll(tP, eP):
    tP.write(0)
    time.sleep(0.0002)

    tP.write(1)
    time.sleep(0.00001)
    tP.write(0)

    while eP.read() == 0:
        pass
    pulse_start = time.time()

    while eP.read() == 1:
        pass
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)
    # print "Distance:", distance, " cm"

    if (distance < 250):
        return 1
    else:
        return 0


def main():
    while (1):
        for (var i in range(0, NUM_SAMPLES)):
            poll(TRIG, ECHO)

        poll(TRIG2, ECHO2)

        time.sleep(1)


if __name__ == "__main__":
    # os.system(
    #     'curl -v -H \'Content-Type: application/json\' -H \'Accept: application/json\' -X POST -d \'{ \"spot\": { \"location\": \"building 10\", \"occupied\": true, \"prev_occupy_duration\": 134 } }\' http://spotev.hack.viasat.io:8080/spot')
    main()

# call(["curl", "-L", "google.com"])
