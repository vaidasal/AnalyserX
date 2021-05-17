# AnalyserX
Data Visualisation and Management Tool for .ulg Files

AnalyserX is primarily made for engineers working with UAVs. You can create a database for all your test sessions, visualise your test results and export reports as PDF for archiving or sharing. It is possible to synchronise several logs on GPS time and visualise results in 2D or 3D. You can choose to view all the points in 3D plot together or view them changing in time (controlled with slider). It is open for easy customisation over plugins.py file.

# Filetypes
The only file type, that can be imported at the moment is .ulg. The file will be then converted (with pyulog) to multiple .csv files and saved to user_data folder. All further functionality of AnalyserX will only use those .csv files.

# GUI
Analyser runs as a local server application. Its based on Flask. This means it is possible to make it available online as a Website.

# Starting
to start run: python run.py
then open 0.0.0.0:5000 in your browser.
AnalyserX was developed on Chrome and Firefox, therefore it's strongly advised to use one of these browsers.

Required Modules are listed in requirements.txt file.

# Docker
Alternatively you can use AnalyserX over Docker. To create a container run "docker-compose up". After that you will be able to start analyser by simply pressing play button in docker dashboard. AnalyserX will be then accessible using 127.0.0.1 in your browser.

<img width="1345" alt="Screenshot 2021-03-05 at 13 34 56" src="https://user-images.githubusercontent.com/51539520/110128922-9c596400-7dc7-11eb-9166-b60ed4173c92.png">

# Plugins
It is possible to calculate special parameters for your use case when importing .ulg files or creating a set by synchronising two log files. Everytime, when a new log or set is added, AnalyserX will look at plugins.py file to see if there are functions, that could be applied for current dataset. Just by editing plugins.py file you can add custom functionality or make changes on imported log files. After editing plugins.py you have to press refresh for every log or set to recalculate data.
As default following parameters will be calculated: distance between two or more vehiches and Lat Lon to XYZ conversion (vehicle_global_position_0 needed), Euler angle (vehicle_attitude_0), ground speed (vehicle_global_position_0), vector length for acceleration (vehicle_local_position_0) and accelerometer (sensor_combined_0). These parameters will be added to log data as 'calculated' topic. If parameter names, needed for calculations, are not found, calculation will not be executed.

# Create a new Project
<img width="1345" alt="Screenshot 2021-03-05 at 13 28 29" src="https://user-images.githubusercontent.com/51539520/110147154-9e2d2280-7ddb-11eb-8323-4435ecd4cfa4.png">


# Main working space
On the left side you can create new test sessions. In the middle you can add tasks for it and later document the results for each task. On the right side you can find/add your log files.
<img width="1348" alt="Screenshot 2021-03-05 at 15 09 21" src="https://user-images.githubusercontent.com/51539520/110148261-e7ca3d00-7ddc-11eb-9404-d713890402c8.png">

<img width="1348" alt="Screenshot 2021-03-05 at 14 00 18" src="https://user-images.githubusercontent.com/51539520/110147108-92d9f700-7ddb-11eb-9194-4324c5c9efce.png">

# Set
If you have multiple logs, made at a similar time, you can create a set of them. In this way you will be able to view all of them in one plot. Time synchronisation is based on parameter 'vehicle_gps_position_0' (by default) or 'timestamp' (checkbox deselected).
<img width="1348" alt="Screenshot 2021-03-05 at 15 04 09" src="https://user-images.githubusercontent.com/51539520/110147317-d2084800-7ddb-11eb-8f22-0056feecbdca.png">

# Visualisation
In order to select parameters for visualisation you have to edit settings page. After selecting parameters, that are useful for your applcation click save. Your selection will be remembered for each log and set. More selected parameters means slower performance of the programm. It is possible to enter default parameters in the project settings (top right corner). These parameters will be selected automatically for every new log.
<img width="1348" alt="Screenshot 2021-03-05 at 15 10 39" src="https://user-images.githubusercontent.com/51539520/110148342-ff092a80-7ddc-11eb-8c34-ba48e6a50378.png">

# 2D Plot
On the left side you can select parameters for left and right axis. You have to click + in order to add it to axis. If you are visualising a set, the number at the beginning of the line represents the ID of the log. The filters are on the right side. You can assign every parameter to each filter. Background color can be changed in the project settings.
![Screenshot 2021-03-05 at 15 12 15](https://user-images.githubusercontent.com/51539520/110149266-1eed1e00-7dde-11eb-9c10-b3a01b8808fb.png)
<img width="1219" alt="Screenshot 2021-03-05 at 15 13 30" src="https://user-images.githubusercontent.com/51539520/110151008-375e3800-7de0-11eb-936e-15bf24a96a31.png">

# 3D Plot
3D Plot has 4 parameters (3 Axes + Color optional). You can filter the time. Default values represent the earliest and the latest possible time. Tail is used for simulation only. Simulation is designed as an interactive option for displaying movement of multiple objects based on time. 
![Screenshot 2021-03-05 at 15 15 19](https://user-images.githubusercontent.com/51539520/110149982-fca7d000-7dde-11eb-8f2e-e96dcd6f4abc.png)

<img width="978" alt="Screenshot 2021-03-05 at 15 15 57" src="https://user-images.githubusercontent.com/51539520/110150985-31685700-7de0-11eb-8c9a-22891574a183.png">

# Time Synchronisation
AnalyserX looks for 'vehicle_gps_position_0' for gps time with timestamp synchronisation. It's calculated only when creating a set. Synchronisation is based on pandas function merge_asof with direction nearest and tolerance of 500ms. At first, timestamp of the first selected dataset will be analysed in order to determine the shortest data sample period. Then the earliest starting time and the latest ending time for all selected logs will be saved. Syncronisation is then based on time series, that is created with these three parameters.

# PDF Export
It is possible to create a test session report in PDF. You can select, which information should be included.

<img width="594" alt="Screenshot 2021-03-05 at 18 28 37" src="https://user-images.githubusercontent.com/51539520/110151316-9fad1980-7de0-11eb-830e-905ba683c5b7.png">

# Moving Files
It is possible to move AnalyserX to different locations on your file system. Links for files and data are relative.

# Backup
You can make Backup files and then later import them back if needed. Its especially usefull when working with docker, because deleting container without backup would result in complete data loss.

# Disclaimer
It is still an early version of AnalyserX. It is not well tested so it might include bugs and other inefficiencies. Many of the functions are expecting certain parameter names. Default names should work with data set made by Pixhawk devices. I am open to improvements and suggestions.

# Thank you
In order to write this program I used a lot of help from different sources.
Big Thank You for Stack Overflow community for all your questions and answers and Corey Shafer for his Flask YouTube tutorial. I'm very thankful for everyone, who contributed to plotly, pyulog and other libraries, that i'm using in this project.
