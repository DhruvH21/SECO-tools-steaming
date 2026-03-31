import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QPlainTextEdit, QTextEdit
from PySide6.QtCore import Qt
from backend.steaming_framework import SteamingFramework
from backend.config import steamer_config
import threading

class BackEnd:
    def __init__(self, steam_config):
        self.config = steam_config
        self.steam_controller = self.__initalize_steam_instance(steam_config["port"], steam_config["BAUDRATE"], steam_config["TIMEOUT"])
    
    def __initalize_steam_instance(self, port, baudrate, timeout):
        steaming_process = SteamingFramework(port=port, baudrate=baudrate, timeout=timeout)
        return steaming_process
    
    def start_steaming_process(self,units,x_feed_rate,y_feed_rate,deg_of_rotation):
        try:
            self.steam_controller.run_process(units,x_feed_rate,y_feed_rate, deg_of_rotation )
        except Exception as e:
            print(f"Failed to start the steaming process with error:{e}")
            
    
    def emergency_stop(self):
        self.steam_controller.emergency_stop()
        

        
class Window(QWidget):
    def __init__(self, steamer_config) -> None:
        super().__init__()
        self.backend = BackEnd(steam_config=steamer_config)
        self.__generate_window()
        
    def __generate_window(self):
        self.setWindowTitle("Steamer Control")
        self.resize(900, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #5257d6;
            }

            QLabel#titleLabel {
                color: white;
                font-size: 30px;
                font-weight: bold;
                padding: 20px;
            }

            QPushButton {
                font-size: 22px;
                font-weight: bold;
                color: white;
                border: none;
                border-radius: 18px;
                padding: 20px;
                min-height: 80px;
                min-width: 260px;
            }

            QPushButton#startButton {
                background-color: #2ECC71;
            }

            QPushButton#startButton:hover {
                background-color: #27AE60;
            }

            QPushButton#estopButton {
                background-color: #E74C3C;
            }

            QPushButton#estopButton:hover {
                background-color: #C0392B;
            }
            
            QPushButton#reset {
                background-color: #E74C3C;
            }
        """)

        self.title_label = QLabel("STEAM PROCESS CONTROLLER")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("START")
        self.start_button.setObjectName("startButton")

        self.estop_button = QPushButton("EMERGENCY STOP")
        self.estop_button.setObjectName("estopButton")
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("reset")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addSpacing(40)
        button_layout.addWidget(self.estop_button)
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(self.title_label)
        main_layout.addSpacing(50)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        self.start_button.clicked.connect(self.handle_button_click)
        self.estop_button.clicked.connect(self.handle_emergency_stop)
        self.reset_button.clicked.connect(self.backend.steam_controller.startup)
        return 
    
    def handle_button_click(self):
        thread = threading.Thread(target=self.backend.start_steaming_process, args=(steamer_config["units"], steamer_config["x_feed_rate"],steamer_config["y_feed_rate"], steamer_config["deg_of_rotation"]), daemon=False)
        thread.start()
        return
    
    def handle_emergency_stop(self):
        self.backend.steam_controller.emergency_stop()
        return 
    
app = QApplication(sys.argv)
window = Window(steamer_config)
window.show()
sys.exit(app.exec())      