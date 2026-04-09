import time 
import serial
# from .config import steamer_config

PORT = "/dev/cu.usbserial-110"
# BAUDRATE = steamer_config["BAUDRATE"]
# TIMEOUT = steamer_config["TIMEOUT"]
MAX_X = 315
MAX_Y = 120
MAX_Z = 43

class SteamingFramework:
    def __init__(self, port, baudrate, timeout):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.estop = False
        self.startup()
        self.pause_state = False
        time.sleep(2)
        pass

    def startup(self):
        self.send_command(f"M5")
        self.estop = False
        self.ser.write(b'\r\n\r\n')
        time.sleep(2)
        
        #reset I/O buffers
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        
        #status check
    
        self.send_command("?")
        time.sleep(2)
        
        
        #Take machine out of alarm state in case it is stuck from previous state, set units and base level configurations. 
        self.send_command("$X")
        self.send_command("G21") #all units in mm
        self.send_command("G90")
        self.send_command("G94")
        time.sleep(2)
        
        #home device
        
        self.send_command("$H")
        self.send_command("G10 L20 P1 X0 Y0 Z0")
        
        #set units and base level configurations again 
        self.send_command("G21") #all units in mm
        self.send_command("G90")
        self.send_command("G94")
        
        #move to starting position for process
        print("moving to start pos")
        self.send_command("G0  X43.07 Y-48 Z8")
        print("moved to start pos")
        

    def wait_until_idle(self):
        while True:
            self.ser.write(b'?')
            line = self.ser.readline().decode(errors="ignore").strip()
            if line:
                print(line)
                if "<Idle" in line:
                    return
            time.sleep(0.1)
        
    def run_process(self, units, x_feed_rate, y_feed_rate , deg_of_rotation, pause_event):
        """
        This function is responsible for running the entire steam cycle autonomously.
        Units specifies rhe number of tools being steamed.
        x_feed_rate specifies the speed of x axis movement, with a maximum of 1800.
        y_feed_rate specifies the speed of the y movement with a maximum of 1800. 
        deg_of_rotation  specifies how much the tool will rotate per steam cycle(must be a multiple of 360).
        """
        if self.estop:                 #checking for emergency stop, no process can run when emergency stop is on.
            print("CANNOT RUN PROGRAM NOW")
            return
        if x_feed_rate > 1800 or y_feed_rate > 1800:  #check that inputted feed 
            print("x or y feed rates EXCEED 1800, UNSAFE TO RUN, STOPPING PROGRAM")
            self.ser.write(b'\x18')
            raise RuntimeError("unsafe x or y feed rates specified in config")
        
        if 360%deg_of_rotation != 0:
            print("deg_of_rotation is not a multiple of 360, UNSAFE TO RUN, STOPPING PROGRAM")
            self.ser.write(b'\x18')
            raise RuntimeError("unsafe degrees of rotation")

        ###move along tool length
        while units > 0 and pause_event.wait():
            #engage steamer
            
            current_deg_of_rot = 360
            while current_deg_of_rot > 1:
                #pause_event.wait()
                self.send_command('M3 S1000')
                time.sleep(1)
                self.send_command(f'$J=G21 G91 Y42 F{y_feed_rate}')
                self.wait_until_idle()
                #pause_event.wait()
                #time.sleep(0.2)
                self.send_command(f'$J=G21 G91 Y-42 F{y_feed_rate}')
                #self.wait_until_idle()
                time.sleep(0.2)
                
                #Enter rotation code here
                self.send_command(f'M5')
                self.send_command(f'$J=G21 G91 A11.765 F1700')
                #self.send_command(f'$J=G21 G91 -2 F1200')
                
                ###
                current_deg_of_rot = current_deg_of_rot - deg_of_rotation
            
            self.send_command(f'$J=G21 G91 X-10 F{x_feed_rate}')
            units = units -1
        
        
        self.send_command(f'$J=G21 G91 X-155 Y-40 F1500')
        
        ####
    def send_command(self, cmd):
        if self.estop:
            raise RuntimeError("NO COMMANDS CAN RUN, E-STOP IS ACTIVE")
        self.ser.write((cmd + "\n").encode())
        time.sleep(0.3)
        
        while self.ser.in_waiting > 0:
            response = self.ser.readline().decode().strip()
            print("Response:", response)

    def pause(self):
        try:
            if self.ser.is_open:
                self.ser.write(b'!')
                self.pause_state = True
        except Exception as e:
            print(f"Could not pause machine with exception: {e}")
    
    def resume(self):
        try:
            if self.ser.is_open and self.pause_state:
                self.ser.write(b'~')
                self.pause_state = False
        except Exception as e:
            print(f"Could not unpause machine with exception: {e}")
    
    
    def emergency_stop(self, reason="E-stop activated"):
        self.estop = True
        try:
            if self.ser.is_open:
                self.ser.write(b'\x18')
                self.ser.flush()
        finally:
            raise RuntimeError(reason)
        
    def get_status(self):
        self.send_command("?")

    def close(self): 
        if self.ser.is_open:
            self.ser.close()


# if __name__ == "__main__":
#     steaming_process = SteamingFramework(port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
#     steaming_process.run_process(steamer_config["units"], steamer_config["x_feed_rate"],steamer_config["y_feed_rate"], steamer_config["deg_of_rotation"] )