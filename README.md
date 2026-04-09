SECO TOOLS STEAMING PROCESS -

    Welcome to the central code base for the SECO tools steaming automation process. This code base comprises of the frontend and backend of the process, in which the frontend launches the panel to control the steaming machine, and the backend handles the the actual application of each feature that is available within the machine. THE BACKEND CODE SHOULD ONLY BE MODIFIED BY DEVELOPERS OR AUTHORIZED PERSONNEL ONLY!!

HOW TO GET STARTED -

    The first step is to configure the machine under the following folder path: backend/config.py

    In this file, these are the fields available to modify:

    1). port:  Navigate to this folder, and first input the port at which the CNC machine is connected to your laptop in the "port" field(on Mac this is available by running the following command on terminal: ls /dev/cu.*, on windows please refer to google to find best method to find connected ports on your system) . This is REQUIRED, and you will not be able to send commands to the machine otherwise. The port should be set as a string.

    2). x_feed_rate, y_feed_rate: You can modify the x and y feed rates to control the speed of the motors when executing the steaming process.  This is and optional change, and is at the discretion of the user.

    3). baudrate: The baudrate is how fast data is sent between the machine and your laptop, the recommended baudrate is: 115200, change at your own discretion.

    4). timeout: The timeout is the value in seconds of how long the code will wait for a read command to return, meaning it specifies how long the machine will wait in idle without receiving any data from the machine until completely giving up and returning the most recent read call. This prevents the machine from hanging for long periods of time. 2 seconds is an ideal timeout interval.

    5). deg_of_rotation: Degrees of rotation is how many degrees the tool will rotate in one singular rotation period. The total rotation of the tool is always 360 to ensure the entire tool is steamed properly, and hence the degrees of rotation MUST be a multiple of 360, otherwise the code WILL FAIL(run time error)!

    6). Units: this field specifies the number of tools being steamed with a maximum of 6. This should be an int.

    With the configurations prepared, you are now ready to execute the code.

HOW TO RUN THE CODE -

    1). In your terminal, navigate to the SECO-tools-steaming file path.

    2). Now, run the following command: python3 -m frontend.main

    3). You will now see health checks return in the console(prints "ok" when machine is running properly), and after a few seconds the startup process will run. The startup process will home the machine, and move the steaming nozzle right above the first tool on the tool holder. The UI will also launch simultaneously, until the steaming nozzle is above the first tool, DO NOT CLICK START ON THE CONTROL PANEL. If for any reason the system does not home properly or move the the first tool on the tool holder properly, click reset and wait for the machine to home itself again. In rare cases, if the homing is not working properly, please turn off the motherboard, disconnect your machine from the board for a few seconds, then reconnect, power on and try again.

    4). On the UI, there is a start button to start the steaming process, and an emergency stop in case the procedure needs to be stopped at any point. After emergency stop, please click reset or close the window, and repeat steps 1-2 to restart the code.

    5). Once an entire cycle has completed(meaning the amount of units specified in the config file are fully steamed), click reset to bring the machine back to the start state to restart the process again.
