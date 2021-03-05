# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 17:59:49 2020

@author: Vaidas Alaune
"""

# import cufflinks as cf
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import math
import pandas as pd

import plotly.express as px
import plotly.io as pio

class Plotly:

    def draw2D(self, dataSet, leftSelected, rightSelected, axRange, theme):

        print('creating 2D plot...')

        timeStamp = dataSet['timestamp']
        angle = ['phi', 'gamma', 'chi', 'euler']

        # Set Ax reverse if z
        axReversed = [False, False]
        zSet = set(["z"])
        lN = []
        for lSel in leftSelected:
            lN.append(lSel.split("__-__")[1])
        rN = []
        for rSel in rightSelected:
            rN.append(lSel.split("__-__")[1])
        if zSet <= set(lN):
            axReversed[0] = True
        if zSet in set(rN):
            axReversed[0] = True

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        for lSel in leftSelected:
            if lSel:
                # check and convert to degree if angle
                if any(ang in lSel for ang in angle):
                    print('angle found1')
                    yData = np.array(dataSet[lSel]) * 180 / (math.pi)
                else:
                    yData = dataSet[lSel]

                fig.add_trace(go.Scatter(x=timeStamp, y=yData,
                                         name=lSel.split("__-__")[1]), secondary_y=False)

        for rSel in rightSelected:
            if rSel:
                # check and convert to degree if angle
                if any(ang in rSel for ang in angle):
                    print('angle found2')
                    yData = np.array(dataSet[rSel]) * 180 / (math.pi)
                else:
                    yData = dataSet[rSel]

                fig.add_trace(go.Scatter(x=timeStamp, y=yData,
                                         name=rSel.split("__-__")[1]), secondary_y=True)

        if axRange[0]:
            fig.update_yaxes(range=[axRange[0], axRange[1]], secondary_y=False)
        if axRange[2]:
            fig.update_yaxes(range=[axRange[2], axRange[3]], secondary_y=True)

        if axReversed[0]:
            fig.update_yaxes(autorange="reversed", secondary_y=False)
        if axReversed[1]:
            fig.update_yaxes(autorange="reversed", secondary_y=True)

        if theme == "dark":
            fig.layout.template = 'plotly_dark'
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="date"), showlegend=True)

        # Define Name
        fileName = 'plot2D.html'
        # if len(rightSelected) >= 1:
        #    fileName = '{}_{}_2D.html'.format(leftSelected[0],rightSelected[0])
        # else:
        #    fileName = '{}_2D.html'.format(leftSelected[0])

        plot(fig, auto_open=True)

    def draw3D(self, dataSet, x, y, z, c, theme):

        print('creating 3D plot...')
        for key in dataSet.keys():
            print(key)

        tracks = []
        for i in range(len(x)):

            if c[i] != '':
                print(c)
                tracks.append(go.Scatter3d(x=dataSet[x[i]], y=dataSet[y[i]],
                                           z=dataSet[z[i]], line_color=dataSet[c[i]],
                                           text=["Time: {}".format(x) for x in dataSet['timestamp']],
                                           marker=dict(size=2, color=dataSet[c[i]],
                                                       colorbar=dict(y=0.1, len=0.8), colorscale="Viridis")))

            else:
                tracks.append(go.Scatter3d(x=dataSet[x[i]], y=dataSet[y[i]],
                                           z=dataSet[z[i]], text=["Time: {}".format(x) for x in dataSet['timestamp']],
                                           marker=dict(size=2)))

        fig = go.Figure(data=tracks)

        if theme == "dark":
            fig.layout.template = 'plotly_dark'
        fig.update_scenes(zaxis_autorange="reversed")
        fig.update_layout(scene_aspectmode='data')
        plot(fig, auto_open=True)



    def X2drawWithSliderReducedSteps(self, dataSet, x, y, z, tailNum, theme):

        print('simulating 3D....')

        tail = 3000
        if tailNum != '':
            tail = int(tailNum)

        def giveColor(step):
            num = step
            if step > tail:
                num = tail
            return list(np.ones(num))

        def combineData(list, step):
            num = 0
            if step < tail:
                num = 0
            else:
                num = step - tail
            l1 = list[0][num:step]
            for l in range(1, len(list)):
                l1.extend(list[l][num:step])
            return l1

        length = len(dataSet)

        stepFactor = 1

        if length > 500:
            stepFactor = int(length / 500)

        time = list(dataSet['timestamp'])
        maxData = {"x": [], "y": [], "z": []}
        minData = {"x": [], "y": [], "z": []}
        xx = []
        yy = []
        zz = []
        for i in range(len(x)):
            maxData["x"].append(max(list(dataSet[x[i]])))
            maxData["y"].append(max(list(dataSet[y[i]])))
            maxData["z"].append(max(list(dataSet[z[i]])))
            minData["x"].append(min(list(dataSet[x[i]])))
            minData["y"].append(min(list(dataSet[y[i]])))
            minData["z"].append(min(list(dataSet[z[i]])))
            xx.append(list(dataSet[x[i]]))
            yy.append(list(dataSet[y[i]]))
            zz.append(list(dataSet[z[i]]))

        aspectX = max(maxData["x"]) - min(minData["x"])
        aspectY = max(maxData["y"]) - min(minData["y"])
        aspectZ = max(maxData["z"]) - min(minData["z"])
        aspSum = aspectX + aspectY + aspectZ
        aspectX = aspectX / aspSum
        aspectY = aspectY / aspSum
        aspectZ = aspectZ / aspSum

        start_index = 0

        # Build all traces with visible=False
        data = [go.Scatter3d(
            visible=False,
            mode='markers',
            marker=dict(size=4, color=giveColor(step), colorscale=[[1, 'red'], [0, 'blue']]),
            # name = str(time[step]),
            x=combineData(xx, step),
            y=combineData(yy, step),
            z=combineData(zz, step))
            for step in range(1, int(len(dataSet)), stepFactor)]

        # Make initial trace visible
        data[start_index]['visible'] = True

        # Build slider steps
        steps = []
        for i in range(int(len(dataSet) / stepFactor) - 1):
            step = dict(
                # Update method allows us to update both trace and layout properties
                method='update',
                label=time[int((i + 1) * stepFactor)],
                args=[
                    # Make the ith trace visible
                    {'visible': [t == i for t in range(int(len(dataSet) / stepFactor))]}])
            steps.append(step)

        # Build sliders
        sliders = [go.layout.Slider(
            active=start_index,
            currentvalue={"prefix": "Time: "},
            pad={"t": 50},
            steps=steps
        )]

        layout = go.Layout(sliders=sliders)

        fig = go.Figure(data=data, layout=layout)

        if theme == "dark":
            fig.layout.template = 'plotly_dark'

        fig.update_layout(scene=dict(xaxis=dict(nticks=4, range=[min(minData["x"]), max(maxData["x"])], ),
                                     yaxis=dict(nticks=4, range=[min(minData["y"]), max(maxData["y"])], ),
                                     zaxis=dict(nticks=4, range=[max(maxData["z"]), min(minData["z"])], ), ),
                          scene_aspectmode='manual', scene_aspectratio=dict(x=aspectX, y=aspectY, z=aspectZ))

        print('red: 1 dataSet')

        plot(fig, auto_open=True)