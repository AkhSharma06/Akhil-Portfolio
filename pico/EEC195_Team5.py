"""
\file       EEC195_Team5.py
\brief      Pico uC code for motor control and sensor interfacing.
            Interfaces with Rasp Pi for motor control instructions

\authors    Corbin Warmbier
            Brian Barcenas
            Akhil Sharma
            Alize De Leon

\date       Initial: 05/17/24  |  Last: 05/22/24
"""

""" [Imports] """
from machine import ADC, Pin, PWM, Timer
from time import sleep
from math import pi


# ========================================= #
#      === [Declarations & Init] ===        #
# ========================================= #

""" [Constants] """
MOTOR_FREQ = 5000  # 5kHz; optimal VNH freq
SERVO_FREQ = 100
MOTOR_SPD_MAX = 200000  # Based on MOTOR_FREQ ! Must Change if MOTOR_FREQ is modified
TIMER_FREQ = 2  # Hz
COUNTS_TO_ROTATION = 3  # Number of counters per wheel rotation (aka # of tape pieces)

""" [Initialization] """
# DC Motor Pin Setup
Motor_PWM = Pin(13, Pin.OUT)
Motor_INA = Pin(14, Pin.OUT)
Motor_INB = Pin(15, Pin.OUT)
Motor_CS = ADC(Pin(28))  # Optional Current Sensing Pin; Analog Read

Servo_PWM = Pin(20, Pin.OUT)  # Servo Motor Pin Setup
Motor_Spd = Pin(22, Pin.IN, Pin.PULL_DOWN)  # Color Sensor for Tracking Speed Pin Setup

# Initialize Pins for PWM and Set Frequency
Motor_PWM = PWM(Motor_PWM, freq = MOTOR_FREQ)
Servo_PWM = PWM(Servo_PWM, freq = SERVO_FREQ)

# Init Globals
timer = Timer()
counter = 0
last_distance = 0
traveled_distance = 0

# ========================================= #
#         === [Local Functions] ===         #
# ========================================= #
def program_header():
    """
    Prints program header on startup
    :return: none
    """
    print("===============================================\n")
    print("=============== [EEC195 Team 5] ===============\n")
    print("===============================================\n")
    print("=                                             =\n")
    print("= Date: 05/17/2024                            =\n")
    sleep(0.3)
    print("= Praying to 100,000 Indian Gods...           =\n")
    sleep(0.3)
    print("= Sacrificing 50 goats...                     =\n")
    sleep(0.3)
    print("= Message sent, program starting              =\n")
    print("===============================================\n")
    sleep(0.3)  # The header must be seen...

def set_motor_dir(direction):
    """
    Sets motor to desired direction. If given invalid direction, motor direction
    will be unaffected.

    :param direction <char>: Sets motor to one of the 3 accepted settings:
        + 'F': Forward
        + 'R': Reverse
        + 'B': Brake
    :return: none
    """
    if direction == 'F' or direction == 'f':
        Motor_INA.value(1)
        Motor_INB.value(0)
    elif direction == 'R' or direction == 'r':
        Motor_INA.value(0)
        Motor_INB.value(1)
    elif direction == 'B' or direction == 'b':
        Motor_INA.value(0)
        Motor_INB.value(0)


def set_motor_spd(percent_spd):
    """
    Sets motor to desired speed as a percent of the MAXIMUM speed.
    !! set_motor_dir SHOULD be called before this function !!

    :param percent_spd <int>: Sets motor to desired speed. Acceptable Range (0% - 100%)
    :return: none
    """
    if percent_spd < 0 or percent_spd > 100:
        return
    duty_cycle = MOTOR_SPD_MAX * percent_spd / 100.0  # Convert Percent Speed to Duty Cycle in ns
    Motor_PWM.duty_ns(int(duty_cycle))


def set_servo(direction, percent_ang=0):
    """
    Sets servo to desired direction and at the percentage of that direction.
    100% percent in a direction correlates to roughly ~ 45 degrees

    :param direction <char>: Sets servo to one of the 3 accepted settings:
        + 'R': Right
        + 'L': Left
        + 'N': Neutral
    :param percent_ang <int>: Turns to a percentage of the maximum angle. Range (0% - 100%)
        * Note: percent_angle is not used in neutral setting. 100% = Max angle ~ 45 degrees
    :return: none
    """
    if percent_ang < 0 or percent_ang > 100:
        return
    if direction == 'R' or direction == 'r':
        # Range (1100000 -> 1500000)
        delta = 400000 * percent_ang
        Servo_PWM.duty_ns(1500000 - delta)
    elif direction == 'L' or direction == 'l':
        # Range (1500000 -> 1900000)
        delta = 400000 * percent_ang
        Servo_PWM.duty_ns(1500000 + delta)
    elif direction == 'N' or direction == 'n':
        Servo_PWM.duty_ns(1500000)


def car_init():
    """
    Initializes all motors to neutral and brakes
    """
    set_motor_dir('N')
    set_motor_spd(0)
    set_servo('N')
    sleep(0.2)


def car_stop():
    car_init()

def spd_irq_handler(edge_type):
    """
    Interrupt handler for speed sensor
    
    :param edge_type <Pin obj>: Falling or rising edge irq detection
    :return: none
    """
    global counter
    counter += 1

def spd_counter(timer):
    global counter
    global traveled_distance
    if counter != 0:
        distance = (counter / COUNTS_TO_ROTATION) * 4.1 * pi  # Distance formula 'Rotations * Wheel Dia * Pi = Inches'
        print(f'Traveled {distance} inches')
        traveled_distance += distance
    counter = 0


# 4.1 inches (diameter of wheel)
# Determine RPM
# Equation: RPM * Wheel Diameter * Pi == Inches / Min
def get_distance():
    global last_distance
    global traveled_distance
    distance = traveled_distance - last_distance
    last_distance = traveled_distance
    print(f'Traveled {distance} inches since last func call')
    return distance

# ========================================= #
#          === [Main Function] ===          #
# ========================================= #
if True:
    # Init
    program_header()
    car_init()
    Motor_Spd.irq(trigger = Pin.IRQ_RISING, handler = spd_irq_handler)
    timer.init(mode = Timer.PERIODIC, freq = TIMER_FREQ, callback = spd_counter)

    # Set Motor to Forward for 30%
    set_motor_dir('F')
    set_motor_spd(30)
    sleep(2)
    
    car_stop()
