import pandas as pd
import numpy as np
from squaternion import Quaternion
from geopy import distance
import fnmatch
import os
import math
from itertools import combinations
from analyser import app


class Plugins:

    def addToMultipleLogs(self, mergedData, set_path, log_list):
        print("addToMultipleLogs")

        mergedData = self.distanceCalc(mergedData, log_list)
        mergedData = self.latLonToXYZ(mergedData, log_list)

        filename = os.path.join(app.root_path, 'static', 'user_data', set_path, 'merged.csv')
        mergedData.to_csv(filename, index=False)


        return

    # Calculate distance between two points and add to merged dataset
    def distanceCalc(self, mergedData, log_list):
        print('calculating distance...')
        topic = 'vehicle_global_position_0'
        parameters = ['lat','lon', 'alt']
        cols = []
        data = mergedData
        for l in log_list:
            for p in parameters:
                cName = str(l) + "__-__" + str(p) + "__-__" + topic
                cols.append(cName)

        if set(cols) <= set(mergedData.keys()):
            lat = "__-__lat__-__" + topic
            lon = "__-__lon__-__" + topic
            alt = "__-__alt__-__" + topic
            dist = [0] * len(mergedData)
            alti = [0] * len(mergedData)
            eucl_dist = [0] * len(mergedData)

            latLonData = []
            for id in log_list:
                logData = {"lat": data[str(id) + lat], "lon": data[str(id) + lon], "alt": data[str(id) + alt], "id": id}
                latLonData.append(logData)

            comb = combinations(range(len(log_list)), 2)
            for c in list(comb):
                for i in range(len(mergedData)):
                    if np.isnan([latLonData[c[0]]["lat"][i], latLonData[c[0]]["lon"][i], latLonData[c[1]]["lat"][i], latLonData[c[1]]["lon"][i]]).any():
                        continue
                    else:
                        dist[i] = distance.geodesic((latLonData[c[0]]["lat"][i], latLonData[c[0]]["lon"][i]), (latLonData[c[1]]["lat"][i], latLonData[c[1]]["lon"][i]), ellipsoid='GRS-80').km
                        dist[i] = dist[i] * 1000
                        alti[i] = (latLonData[c[1]]["alt"][i] - latLonData[c[0]]["alt"][i])
                        eucl_dist[i] = math.sqrt(dist[i] ** 2 + alti[i] ** 2)
                distName = str(latLonData[c[0]]["id"]) + "__-__flat_distance_" + str(latLonData[c[0]]["id"]) + "<->" + str(
                    latLonData[c[1]]["id"]) + "__-__calculated"
                altName = str(latLonData[c[0]]["id"]) + "__-__alt_difference_" + str(latLonData[c[1]]["id"]) + "<->" + str(
                    latLonData[c[0]]["id"]) + "__-__calculated"
                euclName = str(latLonData[c[0]]["id"]) + "__-__eucl_distance_" + str(latLonData[c[0]]["id"]) + "<->" + str(
                    latLonData[c[1]]["id"]) + "__-__calculated"

                data[distName] = dist
                data[altName] = alti
                data[euclName] = eucl_dist


        print('distance complete')

        return (data)


    def latLonToXYZ(self, mergedData, log_list):
        print("calculating lat lon to xyz...")
        topic = 'vehicle_global_position_0'
        parameters = ['lat', 'lon', 'alt']
        cols = []
        data = mergedData
        for l in log_list:
            for p in parameters:
                cName = str(l) + "__-__" + str(p) + "__-__" + topic
                cols.append(cName)

        if set(cols) <= set(mergedData.keys()):
            lat = "__-__lat__-__" + topic
            lon = "__-__lon__-__" + topic
            alt = "__-__alt__-__" + topic

            latLonData = []
            for id in log_list:
                logData = {"lat": data[str(id) + lat], "lon": data[str(id) + lon], "alt": data[str(id) + alt], "id": id}
                latLonData.append(logData)

            x1 = [0] * len(mergedData)
            y1 = [0] * len(mergedData)
            z1 = [0] * len(mergedData)

            for c in range(len(log_list)):
                for i in range(len(mergedData)):
                    if np.isnan([latLonData[c]["lat"][i], latLonData[c]["lon"][i]]).any():
                        continue
                    else:
                        x1[i], y1[i], z1[i] = self.latlon_to_xyz(latLonData[c]["lat"][i], latLonData[c]["lon"][i],
                                                                 latLonData[c]["alt"][i])

                name = str(latLonData[c]["id"]) + "__-__Cartesian_"

                data[name + 'x__-__calculated'] = x1
                data[name + 'y__-__calculated'] = y1
                data[name + 'z__-__calculated'] = z1

        print('lat lon to XYZ conversion completed')

        return (data)

    def latlon_to_xyz(self, lat, lon, alt):
        """Convert angluar to cartesian coordiantes

        latitude is the 90deg - zenith angle in range [-90;90]
        lonitude is the azimuthal angle in range [-180;180]
        """
        # print('lat: {}, lon: {}'.format(lat, lon))

        r = 6371 + (alt * 0.001)
        theta = math.radians(lat)
        phi = math.radians(lon)
        x = ((r * math.cos(theta) * math.cos(phi)) - 4151) * 1000
        y = ((r * math.cos(theta) * math.sin(phi)) - 651.67) * 1000
        z = ((r * math.sin(theta)) - 4789.5) * 1000

        x, y, z = self.rotate3D(x, y, z, math.radians(8.92), math.radians(-41.26), math.radians(0))

        # print('lat: {}, lon: {}, r: {}, x: {}, y: {}, z: {}'.format(lat, lon, r, x,y,z))

        return x, y, z

    def rotate3D(self, x, y, z, rx, ry, rz):
        # Rotation
        xRot = np.array([[1, 0, 0], [0, math.cos(rx), - math.sin(rx)], [0, math.sin(rx), math.cos(rx)]])
        yRot = np.array([[math.cos(ry), 0, math.sin(ry)], [0, 1, 0], [- math.sin(ry), 0, math.cos(ry)]])
        zRot = np.array([[math.cos(rz), - math.sin(rz), 0], [math.sin(rz), math.cos(rz), 0], [0, 0, 1]])
        point = np.array([x, y, z])
        point = xRot.dot(point)
        point = yRot.dot(point)
        point = zRot.dot(point)
        x = point[0]
        y = point[1]
        z = point[2]

        return x, y, z








    def addToOneLog(self, fileName, dirName):
        print("calculating one Log data...")
        (topList, fName) = self.getFileList(fileName,dirName)  # returns list of topic-names and filename (without .csv)
        calcList = []

        ###### EULER ######
        topic = "vehicle_attitude_0"
        if topic in topList:
            filename = fName + '_' + topic + '.csv'
            filename = os.path.join(app.root_path, 'static', 'user_data', dirName, filename)
            data = pd.read_csv(filename)

            calc = {}
            eulerXYZ = self.qatToEul(data["q[0]"], data["q[1]"], data["q[2]"], data["q[3]"])
            calc['eulerX'] = eulerXYZ[0]
            calc['eulerY'] = eulerXYZ[1]
            calc['eulerZ'] = eulerXYZ[2]
            calc['timestamp'] = data['timestamp']
            calc['dateTime'] = pd.to_datetime(data['timestamp'], unit='us').dt.round('ms')
            calc = pd.DataFrame(data=calc)
            calcList.append(calc)

        ###### GROUND SPEED ######
        topic = "vehicle_global_position_0"
        if topic in topList:
            filename = fName + '_' + topic + '.csv'
            filename = os.path.join(app.root_path, 'static', 'user_data', dirName, filename)
            data = pd.read_csv(filename)
            calc = {}
            calc['v_tot'] = self.totalVector(data["vel_n"], data["vel_e"], data["vel_d"])
            sinGa = - data["vel_d"] / calc['v_tot']
            calc['gamma'] = np.arcsin(sinGa)
            calc['timestamp'] = data['timestamp']
            calc['dateTime'] = pd.to_datetime(data['timestamp'], unit='us').dt.round('ms')
            calc = pd.DataFrame(data=calc)
            calcList.append(calc)

        ###### ACCELERATION #####
        topic = "vehicle_local_position_0"
        if topic in topList:
            filename = fName + '_' + topic + '.csv'
            filename = os.path.join(app.root_path, 'static', 'user_data', dirName, filename)
            data = pd.read_csv(filename)
            calc = {}
            calc['a_tot_locPos'] = self.totalVector(data["ax"], data["ay"], data["az"])
            calc['timestamp'] = data['timestamp']
            calc['dateTime'] = pd.to_datetime(data['timestamp'], unit='us').dt.round('ms')
            calc = pd.DataFrame(data=calc)
            calcList.append(calc)

        ###### ACCELEROMETER #####
        topic = "____"
        if topic in topList:
            filename = fName + '_' + topic + '.csv'
            filename = os.path.join(app.root_path, 'static', 'user_data', dirName, filename)
            data = pd.read_csv(filename)
            calc = {}
            calc['a_tot_sc'] = self.totalVector(data['accelerometer_m_s2[0]'], data['accelerometer_m_s2[1]'], data['accelerometer_m_s2[2]'])
            calc['timestamp'] = data['timestamp']
            calc['dateTime'] = pd.to_datetime(data['timestamp'], unit='us').dt.round('ms')
            calc = pd.DataFrame(data=calc)

        data = sorted(calcList, key=len, reverse=True)
        mData = data[0]

        timestamp = mData["timestamp"]
        for d in range(len(data)):
            data[d].drop(columns=['timestamp'], inplace=True)

        for i in range(len(data) - 1):
            mData = pd.merge_asof(left=mData, right=data[i + 1], on='dateTime', direction='nearest',
                                  tolerance=pd.Timedelta('50ms'))

        mData.drop(columns=['dateTime'])
        mData['timestamp'] = timestamp

        # Saving
        filename = fName + '_' + 'calculated.csv'
        filename = os.path.join(app.root_path, 'static', 'user_data', dirName, filename)
        mData.to_csv(filename, index=False)

        print("Data saved")


    # Convert Qaternion -> Euler
    def qatToEul(self, wCol, xCol, yCol, zCol):
        X = []
        Y = []
        Z = []

        for i in range(len(wCol)):
            q = Quaternion(wCol.iloc[i], xCol.iloc[i], yCol.iloc[i], zCol.iloc[i])
            e = list(q.to_euler(degrees=False))
            X.append(e[0])
            Y.append(e[1])
            Z.append(e[2])

        return [X, Y, Z]


    # Calculate total Vector
    def totalVector(self, x, y, z):
       total = np.sqrt(np.square(x) + np.square(y) + np.square(z))
       return total

    def getFileList(self, fileName, dirName):
        listOfCSVs = []
        fName = fileName.split('.')[0]
        dirName = os.path.join(app.root_path, 'static', 'user_data', dirName)
        fLen = len(fName) + 1
        for file in os.listdir(dirName):
            if fnmatch.fnmatch(file, '*.csv'):
                name = file.split('.')[0]
                listOfCSVs.append(name[fLen:])
        return (listOfCSVs, fName)

    def convertTime(self, topList, dirName, fName):
        # calculate time diference between timestamp and gps time
        topic = 'vehicle_gps_position_0'
        timeBetween = pd.Timedelta(seconds=0)
        if topic in topList:
            filename = dirName + '/' + fName + '_' + topic + '.csv'
            data = pd.read_csv(filename)
            GPSTime = pd.to_datetime(data['time_utc_usec'], unit='us').dt.round('ms')
            data['time_utc_usec'] = GPSTime
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='us').dt.round('ms')

            for i in range(len(data)):
                if data['time_utc_usec'][i] != 0:
                    timeBetween = data['time_utc_usec'][i] - data['timestamp'][i]
                    break

        return timeBetween