import matplotlib.pyplot as plot1
import numpy as np
import tkinter as tk
import pandas as pd
from arpaocalc import Ship, ARPA_calculations
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.patches import Circle
from datetime import datetime,timedelta

ls = [30,-30,+60,-60]

def get_arrow(angle):
    a = np.deg2rad(angle)
    ar = np.array([[-.25,-.5],[.25,-.5],[0,.5],[-.25,-.5]]).T
    rot = np.array([[np.cos(a),np.sin(a)],[-np.sin(a),np.cos(a)]])
    return np.dot(rot,ar).T 



def test(window,a,id_main ,rad,t = 0,show_list = False,theta=0):
    
    fig = Figure(figsize = (8, 8),
                dpi = 100)
    canvas = FigureCanvasTkAgg(fig,
                                master = window)
    
    
    plot1 = fig.add_subplot(111)
    #plot1.clear()
    id_list = []
    cpa_dict = dict()
    ship_ls = []
    for msg in a:
        if msg["mmsi"] not in id_list:
            #if msg["shipname"] !=None:
            ship_ls.append(Ship(msg["mmsi"],(msg["lon"],msg["lat"]),msg["speed"],msg["course"]))
            id_list.append(msg['mmsi'])
            if msg['mmsi'] == id_main:
                #msg["heading"] = 240
                tex = "HDG:" + "\t"+  str(msg["heading"]) + "\n" + "\n" +  "SOG:" +"\t"+  str(msg["speed"])+ "\n" + "\n"+ "COG:" + "\t"+ str(msg["course"]) #msg["heading"] #240
                tex2 = "LONG:" "\t" + str(msg["lon"]) + "\n" + "\n" + "LAT:" + "\t"  + str(msg["lat"])
                objectA = ship_ls[-1]
    
    objectA.heading += theta
    tempobject =objectA
    zoom_resolution = 0.0125 #0.25-OG #0.1
    plot1.set_xlim(xmin=objectA.position[0]-zoom_resolution,xmax=objectA.position[0]+zoom_resolution) 
    plot1.set_ylim(ymin=objectA.position[1]-zoom_resolution,ymax=objectA.position[1]+zoom_resolution)
    plot1.plot(objectA.position[0],objectA.position[1] ,marker =get_arrow(90-objectA.heading),color = 'blue', markersize=30)
    plot1.grid()


   
    colors = [(0,1,0,0.5),(1,0.64,0.25),(1,0,0,0.25)]

    for i in range(3):

        c1 = Circle((objectA.position[0],objectA.position[1] ),rad[2-i] ,facecolor=colors[i] )
        c1.set_edgecolor("red")
        
        plot1.add_patch(c1)    
    name = 'INS MUMBAI'
    plot1.text(objectA.position[0]+1,objectA.position[1],name) #0.01


    for i in range(0,len(ship_ls)):
        
        
        if id_list[i] != id_main:
            id = id_list[i]
            objectB = ship_ls[i]
            results = ARPA_calculations(objectA, objectB,m=True, posAatcpa = True, posBatcpa= True)
            #print(objectB.id)
            templis = []
            newlis = []
            for alpha in ls:
                
                tempobject.heading +=alpha
                
                templis.append(ARPA_calculations(tempobject, objectB,m=False, posAatcpa = True, posBatcpa= True))
                tempobject.heading -=alpha
            #print(templis)
            #print(abs(templis[0]['cpa']),round(templis[0]['tcpa'],2),abs(templis[1]['cpa']),round(templis[1]['tcpa'],2),abs(templis[2]['cpa']),round(templis[2]['tcpa'],2),abs(templis[3]['cpa']),round(templis[3]['tcpa'],2))
            plot1.plot(objectB.position[0],objectB.position[1] ,marker =get_arrow(90 -objectB.heading),color = 'magenta', markersize=15)
            plot1.text(objectB.position[0],objectB.position[1],id) #name
            
            if t == 0:

                cpa_dict[id] = [abs(results['cpa']),round(results['tcpa'],2),abs(templis[0]['cpa']),round(templis[0]['tcpa'],2),abs(templis[1]['cpa']),round(templis[1]['tcpa'],2),abs(templis[2]['cpa']),round(templis[2]['tcpa'],2),abs(templis[3]['cpa']),round(templis[3]['tcpa'],2)]
            else:
                tcp = round(results['tcpa'],2)
                min = int(tcp//1)
                sec = round((tcp%1)*60)
                
                ti = (datetime.now() + timedelta(minutes=min,seconds = sec)).time().replace(microsecond=0)
                for i in range(4):
                    tc = round(templis[i]['tcpa'],2)
                    mi = int(tc//1)
                    se = round((tc%1)*60)
                    
                    newlis.append((datetime.now() + timedelta(minutes=mi,seconds = se)).time().replace(microsecond=0))
                cpa_dict[id] = [abs(results['cpa']),ti,abs(templis[0]['cpa']),newlis[0],abs(templis[1]['cpa']),newlis[1],abs(templis[2]['cpa']),newlis[2],abs(templis[3]['cpa']),newlis[3]]
    dic2=dict(sorted(cpa_dict.items(),key= lambda x:x[1][1])) #lambda x:x[1]
 
    res = list(dic2.keys())[0]
    for i in range(len(id_list)):
        if id_list[i]==res:
            objectB = ship_ls[i]
            

            
            results = ARPA_calculations(objectA, objectB,m=True, posAatcpa = True, posBatcpa= True)

            try:

                plot1.plot(results['coord'][2],results['coord'][3] ,marker =get_arrow(90 -objectB.heading),color = 'black', markersize=15)
                plot1.plot([results['coord'][0],results['coord'][2]],[results['coord'][1],results['coord'][3]],'m--')
                plot1.plot([objectB.position[0],results['coord'][2]],[objectB.position[1],results['coord'][3]],'k--')
                plot1.plot([objectA.position[0],results['coord'][0]],[objectA.position[1],results['coord'][1]],'r--')
            except:
                pass
            c = Circle((objectB.position[0], objectB.position[1] ),0.008 ,fill = False )
            c.set_edgecolor("red")
            plot1.add_patch(c)


    df= pd.Series(dic2).to_frame()
    df.columns = ["CPA"]
    
    df2 = df.CPA.apply(pd.Series)
    df2.columns = ["CPA","TCPA","CPA(+30)","TCPA(+30)","CPA(-30)","TCPA(-30)","CPA(+60)","TCPA(+60)","CPA(-60)","TCPA(-60)"]

    cols = list(df2.columns)
    tree =  ttk.Treeview(window)
    tree.place(x=0,y=500)
    tree["columns"] = cols
    for i in cols:
        tree.column(i, anchor="w",width=75)
        tree.heading(i, text=i, anchor='w')
    j = 0
    for index, row in df2.iterrows():
        
        tree.insert("",j+1,text=index,values=list(row))
        j+=1

    # creating the Tkinter canvas
    # containing the Matplotlib figure
 
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack(anchor='se')
    
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                    window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


    T = tk.Text(window, height=5, width=30)
    T.pack(anchor='s')
    T.insert(tk.END, tex)

    T1 = tk.Text(window, height=5, width=30)
    T1.place(x=450,y=800)
    T1.insert(tk.END, tex2)