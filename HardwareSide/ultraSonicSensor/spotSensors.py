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
    currTime = time.time()
    pastTime = time.time()
    countOne = 0
    countTwo = 0
    carOneTime = 0
    carTwoTime = 0

    loc_1 = 'Building10-A'
    loc_2 = 'Building10-B'
    occupiedOne = 0
    occupiedTwo = 0

    while (1):
        for i in range(0, NUM_SAMPLES):
            countOne += poll(TRIG, ECHO)
            time.sleep(0.002)
        if NUM_SAMPLES * SUCCESS_PERCENT < countOne:
            print "Object one found!"
            carOneTime += NUM_SAMPLES * 0.002
            carOneTime += 1.5
            occupiedOne = 1
        else:
            print "Object is not there"
            carOneTime = 0
            occupiedOne = 0

        for i in range(0, NUM_SAMPLES):
            countTwo += poll(TRIG2, ECHO2)
            time.sleep(0.002)
        if NUM_SAMPLES * SUCCESS_PERCENT < countTwo:
            print "Object two found!"
            carTwoTime += NUM_SAMPLES * 0.002
            carTwoTime += 1.5
            occupiedTwo = 1
        else:
            print "Object is not there"
            carTwoTime = 0
            occupiedTwo = 0

        countOne = 0
        countTwo = 0

        currTime = time.time()
        if (currTime - pastTime >= 30):
            s = 'curl -v -H \'Content-Type: application/json\' -H \'Accept: application/json\' -X POST -d \'{{ \"spot\" : {{ \"location\": \"{0}\", \"occupied\": {1}, \"prev_occupy_duration\": {2} }} }} \' http://spotev.hack.viasat.io:8080/spot'.format(
                str(loc_1), str(occupiedOne), str(carOneTime))
            st = 'curl -v -H \'Content-Type: application/json\' -H \'Accept: application/json\' -X POST -d \'{{ \"spot\" : {{ \"location\": \"{0}\", \"occupied\": {1}, \"prev_occupy_duration\": {2} }} }} \' http://spotev.hack.viasat.io:8080/spot'.format(
                str(loc_2), str(occupiedTwo), str(carTwoTime))
            os.system(s)
            os.system(st)
            pastTime = currTime

        time.sleep(1)


if __name__ == "__main__":
    main()
