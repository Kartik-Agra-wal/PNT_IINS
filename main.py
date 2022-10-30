from distutils.util import change_root
from email import message

import matplotlib.pyplot as plt
import numpy as np
from arpaocalc import Ship, ARPA_calculations
from tkinter import *
from tkinter import ttk
from func import test
import threading
import sys
import time

#AIS FUNCTIONS
import socket
from pyais import decode
 
ais_data_list = []

def get_ais_data():
    UDP_IP = "169.254.70.16" #HP-ab0027tx
    UDP_PORT = 12345
     
    sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP

    sock.bind((UDP_IP, UDP_PORT))
    

    i = 0
    while True:
        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            #print("received message: %s" % data)
            #decoded = decode(b"!AIVDM,1,1,,B,15NG6V0P01G?cFhE`R2IU?wn28R>,0*05")
            decoded = decode(data).asdict()

            if decoded['mmsi'] == 419565453:
                i=0
                if i==0:
                    decoded['heading'] = 60
                    decoded['course'] = 60
                    decoded['speed'] = 10
                    print("============Main Ship Detected============")
                    ais_data_list.append(decoded)
                    print(decoded)
                    i = i+1
            #elif decoded['heading'] == 511:
                #continue

            else:
                ais_data_list.append(decoded)
                print(decoded)
                
        
        except Exception as error:
            print ("An error occurred", error)
        except KeyboardInterrupt:
            print('Interrupted')
            #break
            sys.exit(0)
    return decoded


id = 419565453

#trd = threading.Thread(target=get_ais_data, args=()) 
#trd.start()


from DockyardData import dockyard_data

def get_sim_ais_data(dockyard_data):
    for decoded in dockyard_data:
        try:
            #print("1",decoded)
            i=0
            if decoded['mmsi'] == 419565453: 
                if i==0:
                    decoded['heading'] = 60
                    decoded['course'] = 60
                    decoded['speed'] = 10
                    print("============Main Ship Detected============")
                    ais_data_list.append(decoded)
                    #print(decoded)
                    i = i+1
            elif decoded['mmsi'] == (None or 0):
                continue

            #elif decoded['heading'] == 511:
                #continue

            else:
                ais_data_list.append(decoded)
                #print(decoded)
            #print(decoded["shipname"] in decoded)
            time.sleep(0.2)
        except Exception as error_in_data:
            print("error_in_data",error_in_data)
        except KeyboardInterrupt:
            print("Data Reading stopped")
            sim.join()



sim = threading.Thread(target=get_sim_ais_data, args=(dockyard_data,)) 
sim.start()

a = ais_data_list

"""
a= [{'msg_type': 1, 'repeat': 0, 'mmsi': 419001261, 'status': '<NavigationStatus.Moored: 5>', 'turn': None, 'speed': 2.9, 'accuracy': False, 'lon': 73.05, 'lat': 19.085, 'course': 270, 'heading': 511, 'second': 1, 'maneuver': 0, 'spare_1': b'\x00', 'raim': False, 'radio': 49315},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419565453, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': None, 'speed': 3, 'accuracy': False, 'lon': 73.05928, 'lat': 19.029358, 'course': 270.0, 'heading': 511, 'second': 3, 'maneuver': 0, 'spare_1': b'\x00', 'raim': True, 'radio': 262144},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419565458, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': None, 'speed': 3, 'accuracy': False, 'lon': 73.05, 'lat': 18.829358, 'course': 90.0, 'heading': 511, 'second': 3, 'maneuver': 0, 'spare_1': b'\x00', 'raim': True, 'radio': 262144},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419565453, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': None, 'speed': 3, 'accuracy': False, 'lon': 73.05928, 'lat': 19.029358, 'course': 360.0, 'heading': 511, 'second': 4, 'maneuver': 0, 'spare_1': b'\x00', 'raim': True, 'radio': 262144},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419000482, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': 0.0, 'speed': 1, 'accuracy': False, 'lon': 72.915798, 'lat': 18.949165, 'course': 50.4, 'heading': 317, 'second': 4, 'maneuver': 0, 'spare_1': b'\x00', 'raim': False, 'radio': 49376},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419001261, 'status': '<NavigationStatus.Moored: 5>', 'turn': None, 'speed': 3.0, 'accuracy': False, 'lon': 72.88296, 'lat': 18.86736, 'course': 35.7, 'heading': 511, 'second': 3, 'maneuver': 0, 'spare_1': b'\x00', 'raim': False, 'radio': 114852},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419565453, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': None, 'speed': 2, 'accuracy': False, 'lon': 73.05928, 'lat': 19.029353, 'course': 360.0, 'heading': 511, 'second': 5, 'maneuver': 0, 'spare_1': b'\x00', 'raim': True, 'radio': 262144},
{'msg_type': 3, 'repeat': 0, 'mmsi': 419001261, 'status': '<NavigationStatus.Moored: 5>', 'turn': None, 'speed': 2.9, 'accuracy': False, 'lon': 72.88295, 'lat': 18.867372, 'course': 32.2, 'heading': 511, 'second': 4, 'maneuver': 0, 'spare_1': b'\x00', 'raim': False, 'radio': 0},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419001585, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': 0.0, 'speed': 1.0, 'accuracy': False, 'lon': 72.954813, 'lat': 18.972742, 'course': 26.4, 'heading': 33, 'second': 4, 'maneuver': 0, 'spare_1': b'\x00', 'raim': False, 'radio': 98547},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419565453, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': None, 'speed': 2, 'accuracy': False, 'lon': 73.05928, 'lat': 19.029353, 'course': 360.0, 'heading': 511, 'second': 6, 'maneuver': 0, 'spare_1': b'\x00', 'raim': True, 'radio': 262144},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419565453, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': None, 'speed': 1, 'accuracy': False, 'lon': 73.059287, 'lat': 19.029353, 'course': 360.0, 'heading': 511, 'second': 7, 'maneuver': 0, 'spare_1': b'\x00', 'raim': True, 'radio': 262144},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419001261, 'status': '<NavigationStatus.Moored: 5>', 'turn': None, 'speed': 2.8, 'accuracy': False, 'lon': 72.882935, 'lat': 18.867393, 'course': 31.0, 'heading': 511, 'second': 6, 'maneuver': 0, 'spare_1': b'\x00', 'raim': False, 'radio': 3508},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419767000, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': 0.0, 'speed': 7.6, 'accuracy': True, 'lon': 72.8956, 'lat': 18.935967, 'course': 238.0, 'heading': 240, 'second': 6, 'maneuver': 0, 'spare_1': b'\x00', 'raim': False, 'radio': 22072},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419575000, 'status': '<NavigationStatus.UnderWayUsingEngine: 0>', 'turn': None, 'speed': 1, 'accuracy': False, 'lon': 72.971545, 'lat': 19.015558, 'course':48.9, 'heading': 511, 'second': 6, 'maneuver': 0, 'spare_1': b'@', 'raim': False, 'radio': 49308},
{'msg_type': 1, 'repeat': 0, 'mmsi': 419956823, 'status': '<NavigationStatus.UnderWaySailing: 8>', 'turn': None, 'speed': 1, 'accuracy': False, 'lon': 73.248547, 'lat': 19.118387, 'course': 236.8, 'heading': 511, 'second': 11, 'maneuver': 0, 'spare_1': b'\x00', 'raim': False, 'radio': 254}]

#"""
#a = dockyard_data
win= Tk()
win.geometry("1920x1080")
win.attributes('-fullscreen',True)
r1 = [0.033,0.0833,0.1667] #[0.013,0.0233,0.0367] #
r2 = [0.05,0.1,0.2]

def change_time(Checkbutton1):
    if Checkbutton1 ==1:
        clear_frame(win,a,id,r1,t =1)
        test.__defaults__ =  (1,False,0)
    else:
        clear_frame(win,a,id,r1)
        test.__defaults__ =  (0,False,0)

def display_text(entry,r):

    theta= entry.get()
    if theta == '':
        theta = 0
    else:
        theta = float(theta)
    clear_frame(win,a,id,r,theta=theta)

def change_mode(r): 

    clear_frame(win,a,id,r)

def clear_frame(window,a,id_main,rad,t = 0 ,show_list = False,theta=0):
    
    for widgets in window.winfo_children():    
        widgets.destroy()

    test(window,a,id_main,rad,t,theta=theta)
    main(rad)
    #win.after(1000, clear_frame)
def main(rad=r1):
    b0  = ttk.Button(win, text= "Show Graph", command=lambda:  clear_frame(win,a,id,rad))
    b0.place(x=200, y=50)
    b1 = ttk.Button(win, text= "Change orientation +30", command=lambda: clear_frame(win,a,id,rad,theta=30))
    b1.place(x=200, y=100)
    b2 = ttk.Button(win, text= "Change orientation +60", command=lambda: clear_frame(win,a,id,rad,theta=60))
    b2.place(x=200, y=150)  
    b3 = ttk.Button(win, text= "Change orientation -30", command=lambda: clear_frame(win,a,id,rad,theta =-30))
    b3.place(x=200, y=200)
    b4 = ttk.Button(win, text= "Change orientation -60", command=lambda: clear_frame(win,a,id,rad,theta =-60))
    b4.place(x=200, y=250)
    b5 = ttk.Button(win, text= "DAY", command=lambda: change_mode(r1))
    b5.place(x=1400, y=750)
    b5 = ttk.Button(win, text= "NIGHT", command=lambda: change_mode(r2))
    b5.place(x=1500, y=750)

    entry= Entry(win, width= 40)
    entry.focus_set()
    entry.place(x=200,y=300)

    #Create a Button to validate Entry Widget
    b6  = ttk.Button(win, text= "Enter",width= 20, command=lambda: display_text(entry,r1))
    b6.place(x=200,y=350)

    b7 = ttk.Button(win, text = "Global time",command= lambda: change_time(1))
    b7.place(x=300,y=800)

    b8 = ttk.Button(win, text = "local time",command= lambda: change_time(0))
    b8.place(x=200,y=800)

    win.mainloop()


try:
    #clear_frame(win,a,id,rad)
    main()
except Exception as error:
    print(error)
except KeyboardInterrupt:
    print("key stopped")
    sim.join()
    #break
