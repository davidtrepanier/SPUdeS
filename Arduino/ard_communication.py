import pyfirmata
from time import sleep

class ard_communication:
    """ Class that lets us control the motors with Communication to an Arduino with pyfirmata"""

    def __init__(self):
        self.board = pyfirmata.ArduinoMega('COM3')  # port = 'COM3'
        self.alpha0 = -2.7
        self.homingAngle = [[90+self.alpha0, 90+self.alpha0, 90+self.alpha0,
                            90+self.alpha0, 90+self.alpha0, 90+self.alpha0]]
        self.pin1 = 7
        self.pin2 = 8
        self.pin3 = 11
        self.pin4 = 12
        self.pin5 = 5
        self.pin6 = 3
        self.max_angle = 180
        self.min_angle = 0
        self.setUpMotors()

    def setUpMotors(self):
        self.board.digital[self.pin1].mode = pyfirmata.SERVO
        self.board.digital[self.pin2].mode = pyfirmata.SERVO
        self.board.digital[self.pin3].mode = pyfirmata.SERVO
        self.board.digital[self.pin4].mode = pyfirmata.SERVO
        self.board.digital[self.pin5].mode = pyfirmata.SERVO
        self.board.digital[self.pin6].mode = pyfirmata.SERVO

    # Custom angle to set Servo motor angle
    def setServoAngle(self, angle, isRad=0):
        #angle_int = int(angle)
        if isRad:
            rad_to_deg = 180.0/3.1416
            alpha = 90
            beta = 1
        else:
            rad_to_deg = 1
            alpha = 0
            beta = -1

        for i in range(len(angle)):
            self.board.digital[self.pin1].write(180.0-(alpha - angle[i][0]*rad_to_deg*beta))
            self.board.digital[self.pin2].write(alpha + angle[i][1]*rad_to_deg)
            self.board.digital[self.pin3].write(180.0 - (alpha - angle[i][2]*rad_to_deg*beta))
            self.board.digital[self.pin4].write(alpha + angle[i][3]*rad_to_deg)
            self.board.digital[self.pin5].write(180.0 - (alpha - angle[i][4]*rad_to_deg*beta))
            self.board.digital[self.pin6].write(alpha + angle[i][5]*rad_to_deg)
            sleep(0.015)

    def goToHomePosition(self):
        self.setServoAngle(self.homingAngle)
        print("HOMING NOW")

    def goToUpDownPosition(self):
        for i in range(90, 140):
            up = [i, i, i, i, i, i]
            self.setServoAngle(up)
            sleep(0.5)
        for i in range(140, 60):
            down = [i, i, i, i, i, i]
            self.setServoAngle(down)
            sleep(0.5)

        self.goToHomePosition()

    def goToTiltsPosition(self):
        for i in range(90, 170):
            tilt = [i, i, 90, 90, 90, 90]
            self.setServoAngle(tilt)
            sleep(0.5)
        self.goToHomePosition()
        for i in range(90, 170):
            tilt = [90, 90, i, i, 90, 90]
            self.setServoAngle(tilt)
            sleep(0.5)
        self.goToHomePosition()
        for i in range(90, 170):
            tilt = [90, 90, 90, 90, i, i]
            self.setServoAngle(tilt)
            sleep(0.5)
        self.goToHomePosition()


    def goUpPosition(self):
        self.setServoAngle(self.homingAngle)
        for i in range(self.homingAngle, 140):
            self.setServoAngle(i)
            sleep(0.5)

    def getServoAngle(self):
        servo1 = (self.board.digital[self.pin1].read())
        servo2 = (self.board.digital[self.pin2].read())
        servo3 = (self.board.digital[self.pin3].read())
        servo4 = (self.board.digital[self.pin4].read())
        servo5 = (self.board.digital[self.pin5].read())
        servo6 = (self.board.digital[self.pin6].read())

        servoAngles = [servo1, servo2, servo3, servo4, servo5, servo6]
        return servoAngles

    ### FOR TESTING ONLY ###
    #while True:
        #angle = input("Type angle")
        #goToUpDownPosition()

        #goUP(angle)
        #setServoAngle(angle)
        # goToHomePosition()
if __name__ == "__main__":
     # Initialize ard_communication class
     arduino_coms = ard_communication()
     angle = [[0.5, 0.7, 0.9, 0.7, 0.4, 0.5], [0.4, 0.5, 0.6, 0.8, 0.9, 1]]
     arduino_coms.setServoAngle(angle, 1)
     print(arduino_coms.getServoAngle())
     arduino_coms.goToHomePosition()
     print(arduino_coms.getServoAngle())
