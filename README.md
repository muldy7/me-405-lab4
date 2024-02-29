# me-405-lab4
 This repository contains code for ME-405 Lab 4. 

 Lab 4 focused on the implemenetaion of cooperative multitasking for closed loop DC motor controll. The lab utilizes previously created motor driver, encoder reader, control loop, and GUI to drive the step response. 

 cotask and taskshare are used to create the system of cooperative multitasking, and previous motor control functions are modified into a FSMs so two motors can be run simultaneously. Each motor function includes an "Init" state, a "Control loop" state, and "Print" state, and a "Done" state. When the GUI triggers a step response, each FSM cycles the states untill the response is completed, where it is graphed on the GUI. 

 Lab 4 includes the investigation of task timing in the effciacy of the closed loop control. The period of 1 motor control function was veried and the effect on step-response was recorded. 
![Alt text](step_response_10ms.png)
![Alt text](step_response_20ms.png)
![Alt text](step_response_30ms.png)
![Alt text](step_response_50ms.png)
![Alt text](step_response_100ms.png)
