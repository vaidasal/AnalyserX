#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 17:52:38 2020

@author: Vaidas Alaune
"""


import pandas as pd
import numpy as np
from squaternion import Quaternion
from geopy import distance
from datetime import datetime
import math
import statistics

class DataReader:

    def readNamesFromSet(self, path):
        print("readNamesFromSet")

        filename = path + '/' + 'merged.csv'
        data = pd.read_csv(filename)

        cols = data.columns.tolist()
        print(f"cols: {cols}")
        logs = []
        topics = []
        namesDict = {}

        timeStamp = self.getStartEndTime(pd.to_datetime(data['timestamp']).dt.round('ms'), True)

        if 'timestamp' in cols:
            cols.remove('timestamp')

        for c in cols:
            logId = c.split('__-__')[0]
            topic = c.split('__-__')[2]
            logs.append(logId)
            topics.append(topic)

        print(f"logs: {logs}")
        print(f"topics: {topics}")

        logs = set(logs)
        topics = set(topics)

        for log in logs:
            namesDict[log] = {}
            for t in topics:
                namesDict[log][t] = []

        for c in cols:
            topic = c.split('__-__')[2]
            logId = c.split('__-__')[0]
            namesDict[logId][topic].append(c)

        namesDictList = []
        for key in namesDict.keys():
            namesDictList.append(namesDict[key])

        return (namesDict, timeStamp, timeStamp)

    def getStartEndTime(self, time, set):
        timeStamp = list(time.dt.strftime('%H:%M:%S.%f'))
        for t in range(len(timeStamp)):
            timeStamp[t] = str(timeStamp[t])[:-4]
        time = timeStamp
        start = time[0][:-3]
        end = time[-1][:-3]
        return [start, end]

    def readDataNames(self, setNum, dirName, number, namesArray):
        namesDict = {}
        timeStamp = ['00:00:00', '00:00:00']
        timeUtc = ['00:00:00', '00:00:00']

        t = True
        for x in range(len(namesArray)):
            filename = dirName + '/' + number + '_' + namesArray[x] + '.csv'

            try:
                data = pd.read_csv(filename)
            except:
                print('couldnt find: {}'.format(filename))
                continue

            if t:
                timeStamp = self.getStartEndTime(pd.to_datetime(data["timestamp"], unit='us').dt.round('ms'), False)
                t = False

            if "time_utc_usec" in data.columns:
                timeUtc = self.getStartEndTime(pd.to_datetime(data["time_utc_usec"], unit='us').dt.round('ms'), False)
                t = False

            cols = data.columns.tolist()
            if 'timestamp' in cols:
                cols.remove('timestamp')
            for i in range(len(cols)):
                cols[i] = str(setNum) + "__-__" + str(cols[i]) + "__-__" + str(namesArray[x])
            namesDict[namesArray[x]] = cols

        return (namesDict, timeStamp, timeUtc)

    # Read Files:
    def readDataFromDir(self, setNum, dirName, number, namesArray):
        print(f"reading Log Data from {dirName}...")
        dataSet = []
        changeTime = False
        tDelta = 0
        
        for x in range(len(namesArray)):
            filename = dirName + '/' + number + '_' + namesArray[x] + '.csv'

            try:
                data = pd.read_csv(filename)
            except:
                print('couldnt find: {}'.format(filename))
                continue

            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='us').dt.round('ms')
            
            # calculate time diference between timestamp and gps time
            if 'time_utc_usec' in data.columns:
                GPSTime = pd.to_datetime(data['time_utc_usec'], unit='us').dt.round('ms')
                data['time_utc_usec'] = GPSTime

                data['timedelta_stamp_utc'] = GPSTime - data['timestamp']
                changeTime = True
                tDelta = data['timedelta_stamp_utc'].mean()

            # add setNumber and fileNumber to column name
            for col in data.columns:
                if col not in ['timestamp', 'timedelta_stamp_utc']:
                    name = str(setNum) + "__-__" + str(col) + "__-__" + str(namesArray[x])
                    data.rename(columns={col: name}, inplace=True)

            dataSet.append(data)

        #MERGE DATA
        # sort longest at first
        data = sorted(dataSet, key=len, reverse=True)
        mData = data[0]

        for i in range(len(data) - 1):
            mData = pd.merge_asof(left=mData, right=data[i + 1], on='timestamp',
                                  tolerance=pd.Timedelta('1000ms'))

        if changeTime:
            mData['timestamp'] = mData['timestamp'] + tDelta
            print("timestamp corrected with gps time")
        else:
            print("timestamp correction on gps time not available because time_utc_usec parameter could not be found")

        if "timedelta_stamp_utc" in mData.keys():
            mData.drop(columns=["timedelta_stamp_utc"], inplace=True)

        print(f"timestamp range: {mData['timestamp'].iloc[0]} - {mData['timestamp'].iloc[-1]}")
        print("Log reading completed")
        return (mData)


    # Merge Datasets
    def mergeDataSets(self, data1, names1, data2, names2):
        print("merging Datasets...")

        leadData = pd.merge_asof(left=data1, right=data2, on='timestamp', direction='nearest', tolerance=pd.Timedelta('500ms'))
            
        
        namesMerged = self.mergeNameDict(names1,names2)
        
        print('Data Set 1 and 2 Merged')
        return(leadData, namesMerged)

    def mergeNameDict(self, dict1, dict2):
        
        merged = dict(dict1)
        for key in dict1:
            merged[key] = list(merged[key])
            merged[key].extend(list(dict2[key]))
        return merged


    # Create one DataSet that includes all Data
    def mergeData(self, dataSet, setNum, checks):
        print("mergeData with checks...")
        # sort longest at first
        data = sorted(dataSet, key=len, reverse=True)
    
        mData = data[0]

        for i in range(len(data) - 1):
            mData = pd.merge_asof(left=mData, right=data[i + 1], on='timestamp', direction='nearest', tolerance=pd.Timedelta('50ms'))
    
        calcArray = []
        
        if checks[1] == 1:
            matchingEuler = self.filterStrings(mData.columns, ['q[0]','q[1]','q[2]','q[3]'])
            if len(matchingEuler) > 4:
                print('euler got more than 4 arguments -> eulerXYZ could be faulty')
            if matchingEuler != []:
                print('adding Euler')
                q0 = [q for q in matchingEuler if "q[0]" in q]
                q1 = [q for q in matchingEuler if "q[1]" in q]
                q2 = [q for q in matchingEuler if "q[2]" in q]
                q3 = [q for q in matchingEuler if "q[3]" in q]
            
                eulerXYZ = self.qatToEul(mData[q0[0]],mData[q1[0]],mData[q2[0]],mData[q3[0]])
                mData[str(str(setNum) + 'eulerX')] = eulerXYZ[0]
                mData[str(str(setNum) + 'eulerY')] = eulerXYZ[1]
                mData[str(str(setNum) + 'eulerZ')] = eulerXYZ[2]
                calcArray.append(str(str(setNum) + 'eulerX'))
                calcArray.append(str(str(setNum) + 'eulerY'))
                calcArray.append(str(str(setNum) + 'eulerZ'))
        
        
        matchingVel = self.filterStrings(mData.columns, ['vel_n','vel_e','vel_d'])
        # removing unwanted values
        matchingVel = [ x for x in matchingVel if "s" not in x ]
        matchingVel = [ x for x in matchingVel if "i" not in x ]
        
        if len(matchingVel) > 3:
            print('v_tot got more than 3 arguments -> vel_ned or gamma could be faulty')
            print(matchingVel)
            
        if matchingVel != []:
            print('adding ground speed')
            vn = [v for v in matchingVel if "vel_n" in v]
            ve = [v for v in matchingVel if "vel_e" in v]
            vd = [v for v in matchingVel if "vel_d" in v]

            mData[str(str(setNum) + 'v_tot')] = self.totalVector(mData[vn[0]],mData[ve[0]],mData[vd[0]])
            
            print('adding gamma')
            sinGa = - mData[vd[0]]/mData[str(str(setNum) + 'v_tot')]
            mData[str(str(setNum) + 'gamma')] = np.arcsin(sinGa)
            
            calcArray.append(str(str(setNum) + 'v_tot'))
            calcArray.append(str(str(setNum) + 'gamma'))
            
        matchingAx = self.filterStrings(mData.columns, ['ax','ay','az'])
        
        # removing unwanted values
        matchingAx = [ x for x in matchingAx if "_" not in x ]
        
        if len(matchingAx) > 3:
            print('a_tot_locPos got more than 3 arguments -> a_tot_locPos could be faulty')
            print(matchingAx)
        if matchingAx != []:
            print('adding total acceleration')
            ax = [a for a in matchingAx if "ax" in a]
            ay = [a for a in matchingAx if "ay" in a]
            az = [a for a in matchingAx if "az" in a]
            
            mData[str(str(setNum) + 'a_tot_locPos')] = self.totalVector(mData[ax[0]],mData[ay[0]],mData[az[0]])
            calcArray.append(str(str(setNum) + 'a_tot_locPos'))
        
        
        matchingSc = self.filterStrings(mData.columns, ['accelerometer_m_s2[0]','accelerometer_m_s2[1]','accelerometer_m_s2[2]'])
        if len(matchingSc) > 3:
            print('a_tot_sc got more than 3 arguments -> a_tot_sc could be faulty')
            print(matchingSc)
        if matchingSc != []:
            print('adding sensor combined acceleration')
            s0 = [s for s in matchingSc if 'accelerometer_m_s2[0]' in s]
            s1 = [s for s in matchingSc if 'accelerometer_m_s2[1]' in s]
            s2 = [s for s in matchingSc if 'accelerometer_m_s2[2]' in s]
            
            mData[str(str(setNum) + 'a_tot_sc')] = self.totalVector(mData[s0[0]],mData[s1[0]],mData[s2[0]])
            calcArray.append(str(str(setNum) + 'a_tot_sc'))

        print('data merged')
        return (mData, calcArray)
        
    def filterStrings(self, string, substr): 
        return [str for str in string if any(sub in str for sub in substr)] 
    
    # Filter on Channel settings

    def selectedFilter(self, chSett, allDataSet):

        filters = ["fil1","fil2","fil3","fil4","fil5","fil6"]


        def filter10Conditions(key, value, data):
            if key not in data.keys().tolist():
                return np.full(len(data), True)

            if value == '-1':
                cond = data[key] < 0.1
            elif value == '1':
                cond = data[key] > 0.1
            elif value == '0':
                cond = (data[key] > -0.1) & (data[key] < 0.1)
            else:
                cond = np.full(len(data), True)
            return cond

        def filterMinMaxConditions(key, value, data):
            if key not in data.keys().tolist():
                return np.full(len(data), True)

            if value[0].isnumeric():
                print("min is Numeric")
                if value[1].isnumeric():
                    print("max is numeric")
                    cond = (data[key] > float(value[0])) & (data[key] < float(value[1]))
                else:
                    cond = data[key] > float(value[0])
            elif value[1].isnumeric():
                cond = data[key] < float(value[1])
            else:
                cond = np.full(len(data), True)
            return cond

        con = []
        for fil in filters:
            keyName = str(chSett[fil]["Topic"][1]) + "__-__" + chSett[fil]["Parameter"] + "__-__" + chSett[fil]["Topic"][0]
            if fil in ["fil5","fil6"]:
                con.append(filterMinMaxConditions(keyName, chSett[fil]["Value"], allDataSet))
            else:
                con.append(filter10Conditions(keyName, chSett[fil]["Value"], allDataSet))

        filteredData = allDataSet.loc[con[0] & con[1] & con[2] & con[3] & con[4] & con[5]]
        print('data filtered')    
        return filteredData


    # Convert Qaternion -> Euler

    def qatToEul(self, wCol, xCol, yCol, zCol):
        X = []
        Y = []
        Z = []
        
        for i in range(len(wCol)):
            q = Quaternion(wCol.iloc[i],xCol.iloc[i],yCol.iloc[i],zCol.iloc[i])
            e = list(q.to_euler(degrees=False))
            X.append(e[0])
            Y.append(e[1])
            Z.append(e[2])
        
        return [X,Y,Z]
    
    # Calculate total Vector
    def totalVector(self, x, y, z):
        total = np.sqrt(np.square(x) + np.square(y) + np.square(z))
        return total
    
    # Calculate distance between two points and add to merged dataset
    def distanceCalc(self, mergedData, mergedNames):
        
        data = mergedData
        names = mergedNames
        dist = [0] * len(mergedData)
        
        if 'vehicle_global_position_0.csv' in mergedNames.keys():
            print('calculating distance...')
            
            lat1, lon1, lat2, lon2 = self.filterLatLon(data, names)
        
            
            for i in range(len(mergedData)):
                if np.isnan([lat1[i],lon1[i],lat2[i],lon2[i]]).any():
                    continue
                else:
                    dist[i] = distance.geodesic((lat1[i],lon1[i]),(lat2[i],lon2[i]), ellipsoid='GRS-80').km
            
            data['distance'] = dist
            
            names['calculated'].append('distance')
            
        print('distance complete')
        
        return (data, names)
          
    def filterLatLon(self, mergedData, mergedNames):
        
        data = mergedData
        names = mergedNames
        
        matchingLoc = self.filterStrings(names['vehicle_global_position_0.csv'], ['lat','lon'])
        matchingLoc = [ x for x in matchingLoc if "reset" not in x ]
        
        names1 = {}
        names2 = {}
            
        for n in matchingLoc:

            if n[0] == '1':
                if 'lat' in n: 
                    names1['lat'] = n
                elif 'lon' in n:
                    names1['lon'] = n
            elif n[0] == '2':
                if 'lat' in n:    
                    names2['lat'] = n
                elif 'lon' in n:
                    names2['lon'] = n
                        
  
        lat1 = data[names1['lat']]
        lon1 = data[names1['lon']]
        
        lat2 = data[names2['lat']]
        lon2 = data[names2['lon']]
        
        return lat1, lon1, lat2, lon2
    
    def filterAlt(self, mergedData, mergedNames):
        data = mergedData
        names = mergedNames
        
        matchingAlt = self.filterStrings(names['vehicle_global_position_0.csv'], ['alt'])
        
        alt1 = []
        alt2 = []
        
        for n in matchingAlt:
            if len(n) == 5:
                if n[0] == '1':
                    alt1 = data[n]
                elif n[0] == '2':
                    alt2 = data[n]
                
        return alt1, alt2
        
            
    def latLonToXYZ(self, mergedData, mergedNames):
        
        data = mergedData
        names = mergedNames
        
        x1 = [0] * len(mergedData)
        y1 = [0] * len(mergedData)
        z1 = [0] * len(mergedData)
        x2 = [0] * len(mergedData)
        y2 = [0] * len(mergedData)
        z2 = [0] * len(mergedData)
        
        if 'vehicle_global_position_0.csv' in mergedNames.keys():
            print('converting lat lon...')
            
            lat1, lon1, lat2, lon2 = self.filterLatLon(mergedData, mergedNames)
            alt1, alt2 = self.filterAlt(mergedData, mergedNames)
        
            for i in range(len(mergedData)):
                if np.isnan([lat1[i],lon1[i],lat2[i],lon2[i]]).any():
                    continue
                else:
                    x1[i], y1[i], z1[i] = self.latlon_to_xyz(lat1[i],lon1[i], alt1[i])
                    x2[i], y2[i], z2[i] = self.latlon_to_xyz(lat2[i],lon2[i], alt2[i])
                    
            data['1x'] = x1
            data['1y'] = y1
            data['1z'] = z1
            data['2x'] = x2
            data['2y'] = y2
            data['2z'] = z2
            
            for n in ['1x','1y','1z','2x','2y','2z']:
                names['calculated'].append(n)
        
        print('lat lon to XYZ conversion completed')
        
        return (data, names)
        
        
    def latlon_to_xyz(self, lat,lon, alt):
        """Convert angluar to cartesian coordiantes
    
        latitude is the 90deg - zenith angle in range [-90;90]
        lonitude is the azimuthal angle in range [-180;180] 
        """
        #print('lat: {}, lon: {}'.format(lat, lon))
        
        r = 6371 + (alt * 0.001)
        theta = math.radians(lat)
        phi = math.radians(lon)
        x = ((r * math.cos(theta) * math.cos(phi)) - 4151) * 1000
        y = ((r * math.cos(theta) * math.sin(phi)) - 651.67) * 1000
        z = ((r * math.sin(theta)) - 4789.5) * 1000
        
        x, y, z = self.rotate3D(x,y,z, math.radians(8.92),math.radians(-41.26),math.radians(0))
        
        #print('lat: {}, lon: {}, r: {}, x: {}, y: {}, z: {}'.format(lat, lon, r, x,y,z))
        
        return x, y, z
        
    def rotate3D(self, x,y,z, rx, ry, rz):
        # Rotation
        xRot = np.array([[1,0,0],[0,math.cos(rx),- math.sin(rx)],[0, math.sin(rx),math.cos(rx)]])
        yRot = np.array([[math.cos(ry), 0, math.sin(ry)], [0,1,0], [- math.sin(ry),0,math.cos(ry)]])
        zRot = np.array([[math.cos(rz),- math.sin(rz),0], [math.sin(rz),math.cos(rz),0], [0,0,1]])
        point = np.array([x, y, z])
        point = xRot.dot(point)
        point = yRot.dot(point)
        point = zRot.dot(point)
        x = point[0]
        y = point[1]
        z = point[2]

        return x, y, z
