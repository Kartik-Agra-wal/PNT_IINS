
import numpy as np
import tkinter as tk
import pandas as pd
from arpaocalc_v_2 import Ship, ARPA_calculations
from tkinter import *
from tkinter import ttk
from matplotlib.patches import Circle
from datetime import datetime,timedelta


import plotly.graph_objects as go


ls = [30,-30,+60,-60]



def figures_to_html(figs, filename="dashboard.html"):
    with open(filename, 'w') as dashboard:
        dashboard.write("<html><head></head><body>" + "\n")
        for fig in figs:
            inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
            dashboard.write(inner_html)
        dashboard.write("</body></html>" + "\n")


def test(a,id_main ,theta=0,t=0):
    
    id_list = []
    cpa_dict = dict()
    ship_ls = []
    for msg in a:
        if msg["mmsi"] not in id_list:
            ship_ls.append(Ship(msg["mmsi"],(msg["lon"],msg["lat"]),msg["speed"],msg["course"]))
            id_list.append(msg['mmsi'])
            if msg['mmsi'] == id_main:
                tex = "HDG:" + "\t"+  str(msg["heading"]) + "\n" + "\n" +  "SOG:" +"\t"+  str(msg["speed"])+ "\n" + "\n"+ "COG:" + "\t"+ str(msg["course"])
                tex2 = "LONG:" "\t" + str(msg["lon"]) + "\n" + "\n" + "LAT:" + "\t"  + str(msg["lat"])
                objectA = ship_ls[-1]
    


    objectA.heading += theta
    tempobject =objectA
    name = 'INS MUMBAI'

    fig = go.Figure(layout_xaxis_range=[objectA.position[0]-0.25,objectA.position[0]+0.25],layout_yaxis_range=[objectA.position[1]-0.25,objectA.position[1]+0.25])

    fig['layout'].update(width=1000, height=1000, autosize=False)

    
    

    colors = ['red','yellow','green']

    r1 = [0.033,0.0833,0.1667]
    r2 = [0.05,0.1,0.2]
    
   

    sd1 = [dict(type="circle",x0 =objectA.position[0]-r1[2],y0 =objectA.position[1]-r1[2],x1 = objectA.position[0]+r1[2],y1 = objectA.position[1]+r1[2] ,fillcolor=colors[2],opacity=0.2)]
    sd2 = [dict(type="circle",x0 =objectA.position[0]-r1[1],y0 =objectA.position[1]-r1[1],x1 = objectA.position[0]+r1[1],y1 = objectA.position[1]+r1[1] ,fillcolor=colors[1],opacity=0.2)]
    sd3 = [dict(type="circle",x0 =objectA.position[0]-r1[0],y0 =objectA.position[1]-r1[0],x1 = objectA.position[0]+r1[0],y1 = objectA.position[1]+r1[0] ,fillcolor=colors[0],opacity=0.2)]
    
    
    sn1 = [dict(type="circle",x0 =objectA.position[0]-r2[2],y0 =objectA.position[1]-r2[2],x1 = objectA.position[0]+r2[2],y1 = objectA.position[1]+r2[2] ,fillcolor=colors[2],opacity=0.2)]
    sn2 = [dict(type="circle",x0 =objectA.position[0]-r2[1],y0 =objectA.position[1]-r2[1],x1 = objectA.position[0]+r2[1],y1 = objectA.position[1]+r2[1] ,fillcolor=colors[1],opacity=0.2)]
    sn3 = [dict(type="circle",x0 =objectA.position[0]-r2[0],y0 =objectA.position[1]-r2[0],x1 = objectA.position[0]+r2[0],y1 = objectA.position[1]+r2[0] ,fillcolor=colors[0],opacity=0.2)]
        
    
    fig.add_trace(go.Scatter(mode="markers+text",x= [objectA.position[0]],y= [objectA.position[1]] ,marker =dict(symbol = 53,angle = 90 - objectA.heading,color = 'blue', size=15),text=name,textposition="top center"))
    
    for i in range(0,len(ship_ls)):
        if id_list[i] != id_main:
            id = id_list[i]
            objectB = ship_ls[i]

            fig.add_trace(go.Scatter(mode="markers+text",x= [objectB.position[0]],y= [objectB.position[1]] ,marker =dict(symbol = 53,angle = 90 - objectB.heading,color = 'orange', size=15),text=id,textposition="top center")),

            results = ARPA_calculations(objectA, objectB,m=True, posAatcpa = True, posBatcpa= True)
            #print(objectB.id)
            templis = []
            newlis = []
            for alpha in ls:
                
                tempobject.heading +=alpha
                
                templis.append(ARPA_calculations(tempobject, objectB,m=False, posAatcpa = True, posBatcpa= True))
                tempobject.heading -=alpha
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


    dic2=dict(sorted(cpa_dict.items(),key= lambda x:x[1][1]))

    df= pd.Series(dic2).to_frame()
    df.columns = ["CPA"]
    
    df2 = df.CPA.apply(pd.Series)
    df2.columns = ["CPA","TCPA","pos30","TCPA1","neg30","TCPA2","pos60","TCPA3","neg60","TCPA4"]












    fig.update_layout(showlegend=False)


    fig.update_layout(
    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=[{"shapes": sd1+sd2+sd3}],
                    label="Day",
                    method="relayout"

                ),
                dict(
                    args=[{"shapes": sn1+sn2+sn3}],
                    label="Night",
                    method="relayout"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.11,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)

    fig.update_layout(
    annotations=[
        dict(text="Mode:", showarrow=False,
                             x=0, y=1.08, yref="paper", align="left")
    ]
)

    fig2 = go.Figure(data=[go.Table(
        header=dict(values=["Ship"]+list(df2.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df2.index,df2.CPA, df2.TCPA,df2.pos30, df2.TCPA1,df2.neg30, df2.TCPA2,df2.pos60, df2.TCPA3,df2.neg60, df2.TCPA4],
                fill_color='lavender',
                align='left'))
    ])



    figures_to_html([fig, fig2])
    #plot1.text(objectA.position[0]+0.01,objectA.position[1],name)