import time 
import serial
PORT = "/dev/cu.usbserial-10"
BAUDRATE = 115200
TIMEOUT = 2
MAX_X = 315
MAX_Y = 120
MAX_Z = 43
class SteamingFramework:
    def __init__(self, port, baudrate, timeout):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.startup()
        time.sleep(2)
        

    def startup(self):
        self.ser.write(b'\r\n\r\n')
        time.sleep(2)
        self.ser.reset_input_buffer()
        self.send_command("$X")
        self.send_command("G91")
        #self.send_command("$J=G21 G91 X-20 F600")
        #self.send_command("$J=G21 G91 Y2 F600")
        #self.send_command("$J=G21 G91 Z-2 F600")

    def wait_until_idle(self):
        while True:
            self.ser.write(b'?')
            line = self.ser.readline().decode(errors="ignore").strip()
            if line:
                print(line)
                if "<Idle" in line:
                    return
            time.sleep(0.1)
        
    def run_process(self, units=5):
        
        
        #######
        
        ###move along tool length
        while units > 0:
            #engage steamer
            
            deg_of_rot = 360
            while deg_of_rot > 1:
                self.send_command("$J=G21 G91 Y-32 F300")
                self.wait_until_idle()
                time.sleep(0.2)
                self.send_command("$J=G21 G91 Y32 F300")
                self.wait_until_idle()
                time.sleep(0.2)
              
                #Enter rotation code here
                self.send_command("$J=G21 G91 Z2 F300")
                self.send_command("$J=G21 G91 Z-2 F300")
                
                ###
                deg_of_rot = deg_of_rot - 180
            
            self.send_command("$J=G21 G91 X32 F900")
            units = units -1
        ####
    def send_command(self, cmd):
        self.ser.write((cmd + "\n").encode())
        time.sleep(0.3)
        
        while self.ser.in_waiting > 0:
            response = self.ser.readline().decode().strip()
            print("Response:", response)

    def get_status(self):
        pass

    def close(self): 
        if self.ser.is_open:
            self.ser.close()


if __name__ == "__main__":
    steaming_process = SteamingFramework(port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    steaming_process.run_process()