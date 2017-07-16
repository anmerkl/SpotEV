# Import the required libraries
import mraa
import time
import os
from datetime import datetime

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

TEST = 0


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
    curr_Time = time.time()
    past_Time = time.time()
    count_One = 0
    count_Two = 0
    car_One_Time = 0
    car_Two_Time = 0

    loc_1 = 'Building10-A'
    loc_2 = 'Building10-B'
    occupied_Sensor_One = 0
    occupied_Sensor_Two = 0
    occupied_Camera_One = 0
    occupied_Camera_Two = 0

    final_Occupied_One = 0
    final_Occupied_Two = 0

    frequency_Car_One = 0.0
    frequency_Car_Two = 0.0

    now = datetime.now()
    seconds_since_StartOfDay = (
        now - now.replace(hour=8, minute=0, second=0, microsecond=0)).total_seconds()

    while (1):
        timeOne = time.time()
        for i in range(0, NUM_SAMPLES):
            count_One += poll(TRIG, ECHO)
            time.sleep(0.002)

        for i in range(0, NUM_SAMPLES):
            count_Two += poll(TRIG2, ECHO2)
            time.sleep(0.002)

        if NUM_SAMPLES * SUCCESS_PERCENT < count_One:
            print "Object one found!"
            timeTwo = time.time()
            occupied_Sensor_One = 1
        else:
            print "Object is not there"
            occupied_Sensor_One = 0

        if NUM_SAMPLES * SUCCESS_PERCENT < count_Two:
            print "Object two found!"
            occupied_Sensor_Two = 1
        else:
            print "Object is not there"
            occupied_Sensor_Two = 0

        count_One = 0
        count_Two = 0

        with open('out.txt', 'r+') as outFile:
            data = outFile.readlines()
        for x in data:
            if "Status:" in x:
                occupied_Camera_One = x[8:9]
                occupied_Camera_Two = x[10:11]

        if occupied_Camera_One and occupied_Sensor_One:
            car_One_Time += (timeTwo + 1 - timeOne)
            final_Occupied_One = 1
        else if occupied_Camera_One and not occupied_Sensor_One:
            car_One_Time = 0
            final_Occupied_One = 0
        else if not occupied_Camera_One and not occupied_Sensor_One:
            car_One_Time = 0
            final_Occupied_One = 0

        if occupied_Camera_Two and occupied_Sensor_Two:
            timeThree = time.time()
            car_Two_Time += (timeThree + 1 - timeOne)
            final_Occupied_Two = 1
        else if occupied_Camera_Two and not occupied_Sensor_Two:
            car_Two_Time = 0
            final_Occupied_Two = 0
        else if not occupied_Camera_Two and not occupied_Sensor_Two:
            car_Two_Time = 0
            final_Occupied_Two = 0

        curr_Time = time.time()
        if (curr_Time - past_Time >= TIME_TO_SEND):
            s = 'curl -v -H \'Content-Type: application/json\' -H \'Accept: application/json\' -X POST -d \'{{ \"spot\" : {{ \"location\": \"{0}\", \"occupied\": {1}, \"prev_occupy_duration\": {2} }} }} \' http://spotev.hack.viasat.io:8080/spot'.format(
                str(loc_1), str(final_Occupied_One), str(car_One_Time))
            st = 'curl -v -H \'Content-Type: application/json\' -H \'Accept: application/json\' -X POST -d \'{{ \"spot\" : {{ \"location\": \"{0}\", \"occupied\": {1}, \"prev_occupy_duration\": {2} }} }} \' http://spotev.hack.viasat.io:8080/spot'.format(
                str(loc_2), str(final_Occupied_Two), str(car_Two_Time))
            os.system(s)
            os.system(st)
            past_Time = curr_Time

        time.sleep(1)

        time_Now = datetime.now()

        # It is 8 PM which means that we should turn off the service so that we are not using up too much power
        # The service will come back up at 6 AM the following day
        if time_Now.hour >= 20 and time_Now.min > 0:
            occupied_Camera_One = 0
            occupied_Camera_Two = 0
            occupied_Sensor_One = 0
            occupied_Sensor_Two = 0
            final_Occupied_One = 0
            final_Occupied_Two = 0
            car_One_Time = 0
            car_Two_Time = 0

            time.sleep(36000)



# Invoke the main method
if __name__ == "__main__":
    main()
