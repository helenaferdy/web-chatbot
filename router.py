from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
import os
import logging, sys

LOG_LOCATION = 'static/log/debug.log'
os.environ["NTC_TEMPLATES_DIR"] = "/Users/helena/Documents/VSCode/netmiko-network-automation/templates"


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s', 
    handlers=[
        logging.FileHandler(LOG_LOCATION),
        logging.StreamHandler(sys.stdout)
        ])

class Routers:
    def __init__(self, hostname, ip, username, password, secret, ios_os):
        self.hostname = hostname
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.ios_os = ios_os

    def connect(self, command):
        allgood = False
        self.command = command
        device = {
            "device_type": "cisco_ios",
            "ip": self.ip,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
        }
        try:
            self.connection = ConnectHandler(**device)
            logging.info(f"{self.ip} : Connected ")
            try:
                self.connection.enable()
                logging.info(f"{self.ip} : Entered enable mode ")
                allgood = True
            except Exception as e:
                logging.error(f"{self.ip}: Failed to enter enable mode")
        except Exception as e:
            logging.error(f"{self.ip}: Failed to connect")

        if allgood:
            self.connect_command()
            parsed = self.parse()
            self.disconnect()
            if parsed == None:
                parsed = [{'Error ': 'Command failed to parse' }]
            return parsed
        else:
            failed = [{'Error ': 'Connecting to device failed' }]
            return failed
            
            
    def connect_command(self):
        try:
            self.output = self.connection.send_command(self.command)
            logging.info(f"{self.ip} : Command '{self.command}' sent")
        except Exception as e:
            logging.error(f"{self.ip} : Failed to parse command '{self.command}'")
    
    def parse(self):
        try:
            self.parsed_output = parse_output(platform=self.ios_os, command=self.command, data=self.output)
            logging.info(f"{self.ip} : Command '{self.command}' parsed")
            return self.parsed_output
        except Exception as e:
            logging.error(f"{self.ip} : Failed to parse command '{self.command}'")

    def disconnect(self):
        self.connection.disconnect()
        logging.info(f"{self.ip} : Disconnected succcessfully")
