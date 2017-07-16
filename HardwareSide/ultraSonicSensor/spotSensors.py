# Import the required libraries
import mraa
import time
import os

# Set the GPIO pins
TRIG = mraa.Gpio(11)
ECHO = mraa.Gpio(10)
TRIG2 = mraa.Gpio(6)
ECHO2 = mraa.Gpio(5)

TRIG.dir(mraa.DIR_OUT)
ECHO.dir(mraa.DIR_IN)
TRIG2.dir(mraa.DIR_OUT)
ECHO2.dir(mraa.DIR_IN)

# Global constants for samples and success rate
NUM_SAMPLES = 200
SUCCESS_PERCENT = 0.60
TIME_TO_SEND = 45

# Function to call for polling the ultrasonic sensors and seeing if the distance is within some bounds that we set
# to succesfully say that a car is there!


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

# Main method that continuously calls the poll method from above and also handles the curl requests to post the JSON
# object to the web server


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
        timeOne = time.time()
        for i in range(0, NUM_SAMPLES):
            countOne += poll(TRIG, ECHO)
            time.sleep(0.002)

        for i in range(0, NUM_SAMPLES):
            countTwo += poll(TRIG2, ECHO2)
            time.sleep(0.002)

        if NUM_SAMPLES * SUCCESS_PERCENT < countOne:
            print "Object one found!"
            timeTwo = time.time()
            carOneTime += (timeTwo + 2 - timeOne)
            occupiedOne = 1
        else:
            print "Object is not there"
            carOneTime = 0
            occupiedOne = 0

        if NUM_SAMPLES * SUCCESS_PERCENT < countTwo:
            print "Object two found!"
            timeThree = time .time()
            carTwoTime += (timeThree + 0.5 - timeOne)
            occupiedTwo = 1
        else:
            print "Object is not there"
            carTwoTime = 0
            occupiedTwo = 0

        countOne = 0
        countTwo = 0

        currTime = time.time()
        if (currTime - pastTime >= TIME_TO_SEND):
            s = 'curl -v -H \'Content-Type: application/json\' -H \'Accept: application/json\' -X POST -d \'{{ \"spot\" : {{ \"location\": \"{0}\", \"occupied\": {1}, \"prev_occupy_duration\": {2} }} }} \' http://spotev.hack.viasat.io:8080/spot'.format(
                str(loc_1), str(occupiedOne), str(carOneTime))
            st = 'curl -v -H \'Content-Type: application/json\' -H \'Accept: application/json\' -X POST -d \'{{ \"spot\" : {{ \"location\": \"{0}\", \"occupied\": {1}, \"prev_occupy_duration\": {2} }} }} \' http://spotev.hack.viasat.io:8080/spot'.format(
                str(loc_2), str(occupiedTwo), str(carTwoTime))
            os.system(s)
            os.system(st)
            pastTime = currTime

        time.sleep(0.5)


# Invoke the main method
if __name__ == "__main__":
    main()
