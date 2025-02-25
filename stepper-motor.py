# https://ben.akrin.com/driving-a-28byj-48-stepper-motor-uln2003-driver-with-a-raspberry-pi/

import RPi.GPIO as GPIO
import time


class StepperMotor:
    input1 = None
    input2 = None
    input3 = None
    input4 = None
    pins = []
    step_sequence = [[1, 0, 0, 1],
                     [1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]
    step_counter = 0

    def __init__(self, input1, input2, input3, input4, steps=4096):
        self.input1 = input1
        self.input2 = input2
        self.input3 = input3
        self.input4 = input4
        self.pins = [self.input1, self.input2, self.input3, self.input4]

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.input1, GPIO.OUT)
        GPIO.setup(self.input2, GPIO.OUT)
        GPIO.setup(self.input3, GPIO.OUT)
        GPIO.setup(self.input4, GPIO.OUT)

        GPIO.output(self.input1, GPIO.LOW)
        GPIO.output(self.input2, GPIO.LOW)
        GPIO.output(self.input3, GPIO.LOW)
        GPIO.output(self.input4, GPIO.LOW)

    def teardown(self):
        GPIO.output(self.input1, GPIO.LOW)
        GPIO.output(self.input2, GPIO.LOW)
        GPIO.output(self.input3, GPIO.LOW)
        GPIO.output(self.input4, GPIO.LOW)
        GPIO.cleanup()

    def step_left(self, steps, step_delay=0.001):
        self._step(steps, False, step_delay)

    def step_right(self, steps, step_delay=0.001):
        self._step(steps, False, step_delay)

    def _step(self, steps, clockwise=True, step_delay=0.001):
        try:
            for i in range(steps):
                for pin in range(0, len(self.pins)):
                    GPIO.output(self.pins[pin], self.step_sequence[self.step_counter][pin])

                if clockwise:
                    self.step_counter = (self.step_counter - 1) % 8
                else:
                    self.step_counter = (self.step_counter + 1) % 8

                time.sleep(step_delay)

        except:
            self.teardown()
