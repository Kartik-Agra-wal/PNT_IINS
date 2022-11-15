from distutils.util import change_root


import matplotlib.pyplot as plt
import numpy as np
from arpaocalc import Ship, ARPA_calculations
from tkinter import *
from tkinter import ttk
import pandas as pd
import threading
import sys
import time
import math
from datetime import datetime,timedelta
t=0



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


id_main = 419565453

#trd = threading.Thread(target=get_ais_data, args=()) 
#trd.start()


from DockyardData import dockyard_data


def get_sim_ais_data(dockyard_data):
    now = time.time()
    for decoded in dockyard_data:
        
        try:
            #print("1",decoded)
            i=0
            if decoded['mmsi'] == 419565453: 
                if i==0:
                    decoded['heading'] = 60
                    decoded['course'] = 60
                    decoded['speed'] = 10
                    #print("============Main Ship Detected============")
                    ais_data_list.append(decoded)
                    #print(decoded)
                    #i = i+1
            elif decoded['mmsi'] == (None or 0):
                continue

            elif decoded['heading'] == 511:
                continue

            else:
                ais_data_list.append(decoded)
                #print(decoded)
            #print(decoded["shipname"] in decoded)
            time.sleep(0.2)
            later = time.time()
            difference = int(later - now)
            if difference >= 15:
                #clear_frame(win,a,id,rad=r1)
                now = time.time()
        except Exception as error_in_data:
            print("error_in_data",error_in_data)
        except KeyboardInterrupt:
            print("Data Reading stopped")
            sim.join()



sim = threading.Thread(target=get_sim_ais_data, args=(dockyard_data,)) 
sim.start()


import plotly.graph_objects as go


import dash
import dash_daq as daq
from dash.dependencies import Output, Input
from dash import dcc,html
from dash import ctx
from random import random
import plotly

ls = [30,-30,+60,-60]

def angle_markings(pos,rad):
    x =[]
    y = []
    tex = []
    tex_pos = []
    for i in range(0,370,10):
        x.append(pos[0]+rad*math.cos(math.radians(i)))
        y.append(pos[1]+rad*math.sin(math.radians(i)))
        if i!=360:
            tex.append(str(i))
            if i<180:
                tex_pos.append("top center")
            else:
                tex_pos.append("bottom center")
    return x,y,tex,tex_pos
    
def test(ais_data_list,theta=0,mode = "day"):
    roc = []
    id_list = []
    cpa_dict = dict()
    ship_ls = []
    name_ls= []
    for msg in ais_data_list:
        if msg["mmsi"] not in id_list:
            ship_ls.append(Ship(msg["mmsi"],(msg["lon"],msg["lat"]),msg["speed"],msg["course"]))
            id_list.append(msg['mmsi'])
            try:
                name_ls.append(msg["shipname"])
            except:
                name_ls.append(msg['mmsi'])
            if msg['mmsi'] == id_main:
                tex = "HDG:" + "\t"+  str(msg["heading"]) + "\n" + "\n" +  "SOG:" +"\t"+  str(msg["speed"])+ "\n" + "\n"+ "COG:" + "\t"+ str(msg["course"])
                tex2 = "LONG:" "\t" + str(msg["lon"]) + "\n" + "\n" + "LAT:" + "\t"  + str(msg["lat"])
                objectA = ship_ls[-1]
    


    objectA.heading += theta
    tempobject =objectA
    name = 'INS MUMBAI'
    zoom_resolution = 0.0125
    fig = go.Figure(layout_xaxis_range=[objectA.position[0]-zoom_resolution,objectA.position[0]+zoom_resolution],layout_yaxis_range=[objectA.position[1]-zoom_resolution,objectA.position[1]+zoom_resolution])

    fig['layout'].update(width=1000, height=1000, uirevision = True)

    
    

    colors = ['red','yellow','green']

    r1 = [0.033/20,0.0833/20,0.1667/20]
    r2 = [0.05/20,0.1/20,0.2/20]
    
   
    if mode == "day":
        fig.add_shape(type="circle",x0 =objectA.position[0]-r1[2],y0 =objectA.position[1]-r1[2],x1 = objectA.position[0]+r1[2],y1 = objectA.position[1]+r1[2] ,fillcolor=colors[2],opacity=0.2,)
        fig.add_shape(type="circle",x0 =objectA.position[0]-r1[1],y0 =objectA.position[1]-r1[1],x1 = objectA.position[0]+r1[1],y1 = objectA.position[1]+r1[1] ,fillcolor=colors[1],opacity=0.2)
        fig.add_shape(type="circle",x0 =objectA.position[0]-r1[0],y0 =objectA.position[1]-r1[0],x1 = objectA.position[0]+r1[0],y1 = objectA.position[1]+r1[0] ,fillcolor=colors[0],opacity=0.2)
        x_a,y_a,tex_a,tex_pos = angle_markings(objectA.position,r1[2])
        fig.add_trace(go.Scatter(
        x=x_a,
        y=y_a,

        mode="markers+text",
        name="Markers and Text",
        marker =dict(symbol = 0,color = 'blue', size=1),text=tex_a,textposition=tex_pos,textfont_size = 10),
    )
    
    else:
        fig.add_shape(type="circle",x0 =objectA.position[0]-r2[2],y0 =objectA.position[1]-r2[2],x1 = objectA.position[0]+r2[2],y1 = objectA.position[1]+r2[2] ,fillcolor=colors[2],opacity=0.2)
        fig.add_shape(type="circle",x0 =objectA.position[0]-r2[1],y0 =objectA.position[1]-r2[1],x1 = objectA.position[0]+r2[1],y1 = objectA.position[1]+r2[1] ,fillcolor=colors[1],opacity=0.2)
        fig.add_shape(type="circle",x0 =objectA.position[0]-r2[0],y0 =objectA.position[1]-r2[0],x1 = objectA.position[0]+r2[0],y1 = objectA.position[1]+r2[0] ,fillcolor=colors[0],opacity=0.2)
        x_a,y_a,tex_a,tex_pos = angle_markings(objectA.position,r2[2])
        fig.add_trace(go.Scatter(
        x=x_a,
        y=y_a,

        mode="markers+text",
        name="Markers and Text",
        marker =dict(symbol = 0,color = 'blue', size=1),text=tex_a,textposition=tex_pos,textfont_size = 10),
    )            

    fig.add_trace(go.Scatter(mode="markers+text",x= [objectA.position[0]],y= [objectA.position[1]] ,marker =dict(symbol = 53,angle = 90 - objectA.heading,color = 'blue', size=15),text=name,textposition="top center"))
    max_roc = None
    riskiest_ship = None
    for i in range(0,len(ship_ls)):
        if id_list[i] != id_main:
            id = id_list[i]
            objectB = ship_ls[i]
            names = name_ls[i]
            fig.add_trace(go.Scatter(mode="markers+text",x= [objectB.position[0]],y= [objectB.position[1]] ,marker =dict(symbol = 53,angle = 90 - objectB.heading,color = 'orange', size=15),text=names,textposition="top center"))

            results = ARPA_calculations(objectA, objectB,m=False, posAatcpa = True, posBatcpa= True)
            if max_roc is None or results['roc'] > max_roc:
                    max_roc = results['roc']
                    riskiest_ship = objectB
            roc.append([id,round(results['roc'],2)])

            templis = []
            newlis = []
            for alpha in ls:
                
                tempobject.heading +=alpha
                
                templis.append(ARPA_calculations(tempobject, objectB,m=False, posAatcpa = True, posBatcpa= True))
                tempobject.heading -=alpha
            if t == 0:

                cpa_dict[names] = [abs(results['cpa']),round(results['tcpa'],2),abs(templis[0]['cpa']),round(templis[0]['tcpa'],2),abs(templis[1]['cpa']),round(templis[1]['tcpa'],2),abs(templis[2]['cpa']),round(templis[2]['tcpa'],2),abs(templis[3]['cpa']),round(templis[3]['tcpa'],2)]
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
                cpa_dict[names] = [abs(results['cpa']),ti,abs(templis[0]['cpa']),newlis[0],abs(templis[1]['cpa']),newlis[1],abs(templis[2]['cpa']),newlis[2],abs(templis[3]['cpa']),newlis[3]]
    
    riskiest = ARPA_calculations(objectA, riskiest_ship,m=True, posAatcpa = True, posBatcpa= True)
    try:
        coords = riskiest['coord']
        fig.add_trace(go.Scatter(mode="markers+text",x= [coords[0]],y= [coords[1]] ,marker =dict(symbol = 53,angle = 90 - objectA.heading,color = 'black', size=15)))
        fig.add_trace(go.Scatter(mode="markers+text",x= [coords[2]],y= [coords[3]] ,marker =dict(symbol = 53,angle = 90 - riskiest_ship.heading,color = 'red', size=15)))
        fig.add_shape(type='line',
                x0=objectA.position[0],
                y0=objectA.position[1],
                x1=coords[0],
                y1=coords[1],
                line=dict(color='black',dash="dot"),
                xref='x',
                yref='y')

        fig.add_shape(type='line',
                x0=riskiest_ship.position[0],
                y0=riskiest_ship.position[1],
                x1=coords[2],
                y1=coords[3],
                line=dict(color='magenta',dash="dot"),
                xref='x',
                yref='y')
    
        

    except:
        pass

    
    
    
    rocdf = pd.DataFrame(roc,columns = ["Ship","ROC"])

    rocdf=rocdf.sort_values(by='ROC', ascending=False)
    

    dic2=dict(sorted(cpa_dict.items(),key= lambda x:x[1][1]))

    df= pd.Series(dic2).to_frame()
    df.columns = ["CPA"]
    
    df2 = df.CPA.apply(pd.Series)
    df2.columns = ["CPA","TCPA","pos30","TCPA1","neg30","TCPA2","pos60","TCPA3","neg60","TCPA4"]



    fig.update_layout(showlegend=False)
    fig.update_layout(title=dict(text="<b>MAP</b>"))
    fig2 = go.Figure(data=[go.Table(
        header=dict(values=["Ship"]+list(df2.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df2.index,df2.CPA, df2.TCPA,df2.pos30, df2.TCPA1,df2.neg30, df2.TCPA2,df2.pos60, df2.TCPA3,df2.neg60, df2.TCPA4],
                fill_color='lavender',
                align='left'))
    ])
    fig2.update_layout(title=dict(text="<b>SHIP LIST</b>"),uirevision = True)
    fig3 = go.Figure(data=[go.Table(
        header=dict(values=list(rocdf.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[rocdf.Ship,rocdf.ROC],
                fill_color='lavender',
                align='left'))
    ])
    
    fig3.update_layout(title=dict(text="<b>Priority List</b>"),uirevision = True )
    
    return fig,fig2,fig3    






app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("PNT"),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,
            n_intervals=0),
    html.Div([
        daq.BooleanSwitch(id="btn1", on=False, color="red",label="+30",labelPosition="bottom",style={'display': 'inline-block'}),
        daq.BooleanSwitch(id="btn2", on=False, color="red",label = "-30",labelPosition="bottom",style={'display': 'inline-block'}),
        daq.BooleanSwitch(id="btn3", on=False, color="red",label = "+60",labelPosition="bottom",style={'display': 'inline-block'}),
        daq.BooleanSwitch(id="btn4", on=False, color="red",label = "-60",labelPosition="bottom",style={'display': 'inline-block'}),
        daq.BooleanSwitch(id="Night", on=False, color="red",label = "Night Mode",labelPosition="bottom")]),
    html.Div(id='container-button-timestamp'),
        dcc.Graph(id='live-update-graph-scatter',style={'display': 'inline-block'}),
        dcc.Graph(id='ROC-table',className="column",style={'display': 'inline-block','width':"33%"}),
        dcc.Graph(id='live-table',className="four columns")
    ])



@app.callback(Output('live-update-graph-scatter', 'figure'),
                Output('live-table', 'figure'),
                Output('ROC-table', 'figure'),
                Output('btn1', 'on'),
                Output('btn2', 'on'),
                Output('btn3', 'on'),
                Output('btn4', 'on'),
              [Input('interval-component', 'n_intervals')],
                Input('btn1', 'on'),
                Input('btn2', 'on'),
                Input('btn3', 'on'),
                Input('btn4', 'on'),
                Input('Night', 'on'))
def app_calback(value,btn1,btn2,btn3,btn4,Night):
    if Night:
        mode = "night"
    else:
        mode = "day"
    if btn1:
        btn2,btn3,btn4 = 0,0,0
        fig,fig2,fig3  =test(ais_data_list,theta = +30,mode=mode)

    elif btn2:
        btn1,btn3,btn4 = 0,0,0
        fig,fig2,fig3  =test(ais_data_list,theta = -30,mode=mode)
    elif btn3:
        btn1,btn2,btn4 = 0,0,0
        fig,fig2,fig3  =test(ais_data_list,theta = +60,mode=mode)
    elif btn4:
        btn1,btn2,btn3 = 0,0,0
        fig,fig2,fig3  =test(ais_data_list,theta = -60,mode=mode)
    else:
        fig,fig2,fig3 = test(ais_data_list,theta= 0,mode=mode)

    return fig,fig2,fig3,btn1,btn2,btn3,btn4



app.run_server(debug=True)