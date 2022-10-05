from email import message
import matplotlib.pyplot as plt
import numpy as np
from arpaocalc import Ship, ARPA_calculations
from tkinter import *


def get_arrow(angle):
    a = np.deg2rad(angle)
    ar = np.array([[-.25,-.5],[.25,-.5],[0,.5],[-.25,-.5]]).T
    rot = np.array([[np.cos(a),np.sin(a)],[-np.sin(a),np.cos(a)]])
    return np.dot(rot,ar).T 



def test(a,id_main,show_list = False,theta=0):
    plt.close()

    id_list = []
    tcpa_dict = dict()
    ship_ls = []
    for msg in a:
        if msg["mmsi"] not in id_list:
            ship_ls.append(Ship(msg["mmsi"],(msg["lon"],msg["lat"]),msg["speed"],msg["course"]))
            id_list.append(msg['mmsi'])
            if msg['mmsi'] == id_main:
                objectA = ship_ls[-1]
    objectA.heading += theta
    plt.xlim(xmin=objectA.position[0]-0.25,xmax=objectA.position[0]+0.25)
    plt.ylim(ymin=objectA.position[1]-0.25,ymax=objectA.position[1]+0.25)
    plt.plot(objectA.position[0],objectA.position[1] ,marker =get_arrow(90-objectA.heading),color = 'blue', markersize=15)
    plt.grid()


    txt = 'ship list \n'

    for i in range(4):

        c1 = plt.Circle((objectA.position[0],objectA.position[1] ),(i+1)*0.08 ,fill = False )
        c1.set_edgecolor("green")
        plt.gcf().gca().add_artist(c1)    
    name = 'INS MUMBAI'
    plt.text(objectA.position[0]+0.01,objectA.position[1],name)


    for i in range(0,len(ship_ls)):
        
        
        if id_list[i] != id_main:
            id = id_list[i]
            objectB = ship_ls[i]
            #print(objectB.heading)
            results = ARPA_calculations(objectA, objectB,m=True, posAatcpa = True, posBatcpa= True)
            str1 = 'cpa:' +str(round(results['cpa'],3)) + 'tcpa: '+ str(round(results['tcpa'],3))
            plt.plot(objectB.position[0],objectB.position[1] ,marker =get_arrow(90 -objectB.heading),color = 'orange', markersize=15)
            plt.text(objectB.position[0],objectB.position[1],str1)
            txt += str(id_list[i]) +" " + str1 + "\n"+ results['status']+'\n'
            tcpa_dict[id] = abs(results['cpa'])
    print(tcpa_dict)
    dic2=dict(sorted(tcpa_dict.items(),key= lambda x:x[1]))
    print("-------")
    print(dic2)
    res = list(dic2.keys())[0]
    for i in range(len(id_list)):
        if id_list[i]==res:
            objectB = ship_ls[i]
            
            # print(objectA.position)
            # print("---------")
            # print(objectB.position)
            
            results = ARPA_calculations(objectA, objectB,m=True, posAatcpa = True, posBatcpa= True)

            try:
                print(results['coord'])
                plt.plot(results['coord'][0],results['coord'][1] ,marker =get_arrow(90 -objectA.heading),color = 'red', markersize=15)
                plt.text(results['coord'][0]+0.01,results['coord'][1],name)
                plt.plot(results['coord'][2],results['coord'][3] ,marker =get_arrow(90 -objectB.heading),color = 'black', markersize=15)
                plt.plot([results['coord'][0],results['coord'][2]],[results['coord'][1],results['coord'][3]],'m--')
                plt.plot([objectB.position[0],results['coord'][2]],[objectB.position[1],results['coord'][3]],'k--')
                plt.plot([objectA.position[0],results['coord'][0]],[objectA.position[1],results['coord'][1]],'r--')
            except:
                pass
            c = plt.Circle((objectB.position[0], objectB.position[1] ),0.008 ,fill = False )
            c.set_edgecolor("red")
            plt.gcf().gca().add_artist(c)


    if show_list:
        ws = Tk()
        ws.title('SHIPS LIST')
        ws.geometry('400x300')
        ws.config(bg='#A67449')
        message = txt
        text_box = Text(
            ws,
            height=26,
            width=80
        )
        text_box.pack(expand=True)

        text_box.insert('end', message)

        ws2 = Tk()
        ws2.title('rank')
        ws2.geometry('400x300')
        ws2.config(bg='#A67449')
        message = dic2
        text_box2 = Text(
            ws2,
            height=26,
            width=80
        )
        text_box2.pack(expand=True)

        text_box2.insert('end', message)
    print("ends")
    plt.show()