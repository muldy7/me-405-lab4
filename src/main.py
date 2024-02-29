"""!
@file main.py
    This file contains our main code to test two different motors cooperatively.
    We used some code from "basic_tasks.py" but modified it to fit our needs.
    This is the file that is stored on the Nucleo microcontroller.

@author JR Ridgely, Abe Muldrow, Lucas Rambo, Peter Tomson
@date   2021-Dec-15 JRR Created from the remains of previous example
@date February 29, 2024 
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
from controller import Controller
from motor_driver import MotorDriver
from encoder_reader import EncoderReader
import utime


def task1_fun(shares):
    """!
    Task that controls the motion of the first motor.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares
    
    state = 0
    
    while True:
        if state == 0:
            motor1=MotorDriver('PC1','PA0','PA1',5)
            encoder1=EncoderReader('PC6','PC7',8)
            controller1=Controller(3300,1,encoder1)
            state = 1 # transition always
            yield
        elif state == 1:
            print('awaiting input')
            #Kp=float(input('Input a Value for Kp: '))
            Kp = 1	# <---- this is where Kp is 
            controller1.set_Kp(Kp)
            state = 2
            yield
        elif state == 2:
            for i in range(100):
                # utime.sleep_ms(1) should need this
                controller1.input_obj.read()
                meas_output=controller1.input_obj.pos
                #print(meas_output)
                
                controller1.run(meas_output)
                PWM=controller1.PWM
                
                motor1.set_duty_cycle(PWM)
                if i == 99:
                    state = 3
                    controller1.input_obj.zero()
                    motor1.set_duty_cycle(0)
                    yield
                else:
                    yield
                yield
                
        elif state == 3:
            # have to know which motor is printing
            #print('printing motor1')
            #controller1.step_response()
            state = 4
            yield
        elif state == 4:
            yield
        
            

def task2_fun(shares):
    """!
    Task for testing the use of tasks during set up of our code
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    the_share, the_queue = shares
    yield
    while True:
        #print("im task two and im doing something")
        yield

def task3_fun(shares):
    """!
    Task that controls the motion of the second motor
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares

    state = 0
    
    while True:
        if state == 0:
            motor2=MotorDriver('PA10','PB4','PB5',3)
            encoder2=EncoderReader('PB6','PB7',4)
            controller2=Controller(3300,1,encoder2)
            state = 1 # transition always
            yield
        elif state == 1:
            print('awaiting input')
            #Kp=float(input('Input a Value for Kp: '))
            Kp = 0.1 # <---- this is where Kp is 
            controller2.set_Kp(Kp)
            state = 2
            yield
        elif state == 2:
            for i in range(100):
                # utime.sleep_ms(1) should need this
                controller2.input_obj.read()
                meas_output=controller2.input_obj.pos
                #print(meas_output)
                
                controller2.run(meas_output)
                PWM=controller2.PWM
                
                motor2.set_duty_cycle(PWM)
                if i == 99:
                    state = 3
                    controller2.input_obj.zero()
                    motor2.set_duty_cycle(0)
                    yield
                else:
                    yield
                yield
        elif state == 3:
            # print the results
            print('start')
            for i in range(len(controller2.pos_output)):
                print(i*35,controller2.pos_output[i])
                yield
            print('end')
            state = 4
            yield
        elif state == 4:
            yield
        


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=2, period=10,
                        profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=3, period=10,
                        profile=True, trace=False, shares=(share0, q0))
    task3 = cotask.Task(task3_fun, name="Task_3", priority=1, period=15,
                        profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')

