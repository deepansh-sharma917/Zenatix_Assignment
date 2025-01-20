

Created By: Deepansh Sharma <br>
Description : It includes all the required steps to execute the  project assignment  <br>
Creation Dt :19-Jan-2025  <br>
Step 1: Database Design Database Schema: Use a database  SQLite  to store the data. You need tables for storing sensor <br>
readings, metadata (e.g., site and meter info), and any processed <br>
metrics.  <br>
CREATE TABLE Sites ( site_id VARCHAR(100) PRIMARY KEY, <br>
site_name VARCHAR(100) );  <br>
CREATE TABLE Meters ( meter_id TEXT PRIMARY <br>
KEY, site_id TEXT,  <br>
FOREIGN KEY (site_id) REFERENCES sites(site_id) ); <br>
CREATE TABLE Sensor_Data ( id INTEGER PRIMARY KEY AUTOINCREMENT, <br>
site_id 
VARCHAR(100), <br>
meter_id VARCHAR(100), <br>
timestamp VARCHAR(100),<br> 
sensor_name VARCHAR(100),<br>
sensor_value FLOAT(10,2), <br>
status TEXT, <br>
year int(10), <br>
month int(10), <br>
week_no int(10), <br>
period int(10), <br>
FOREIGN KEY (site_id) REFERENCES sites (site_id), <br>
FOREIGN KEY (meter_id) REFERENCES meters (meter_id) ); 
CREATE TABLE Period_Metrics<br>
( site_id TEXT, <br>
period INTEGER, <br>
year INTEGER, <br>
average_consumption FLOAT(10,2), <br>
max_consumption FLOAT(10,2),<br>
total_consumption FLOAT(10,2), <br>
FOREIGN KEY (site_id) REFERENCES sites (site_id) ); 
Modular Object Oriented Solution <br>
a. Class Descriptions <br>
1.DataLoader -Loads data from the provided CSV file.<br>
 -Cleans and preprocesses the data: -Handles missing or inconsistent<br>
  data. -Flags and filters out invalid sensor values (e.g., negative<br>
  values for temperature or power consumption). -Removes duplicate rows
  and missing columns. -Loads the cleaned data into the database.<br>
2.DatabaseHandler: <br>
   -Manages database connection and execution of<br>
    queries. <br>
    -Loads cleaned data into the database. <br>
3.DataPreProcessor:<br>
   Fetches data from the database. <br>
    -Processes data using Pandas and NumPy:<br>
    -Normalizes sensor values (e.g., scales power consumption values between 0 and 1). <br>
    -Creates a time-series DataFrame with timestamps as the index.<br>
    -Fills missing timestamps using interpolation. 4.MetricsCalculator:<br>
    -Calculates metrics such as averages, maximums, and daily sums. <br>
    -Stores  metrics in the database for visualization.<br>
5.GraphGenerator:<br>
-Generates plots/visualizations from the metrics data:<br>
-Average consumption.<br>
 -Maximum consumption.<br>
  -Total power consumption. <br>
  -Saves plots as PNG files. <br>
6.DataReportGenerator: <br>
-Exports calculated metrics into a CSV report for stakeholders. <br>
Challenges and Solutions <br>
 -Challenge: Handling large datasets and ensuring data integrity. <br>
 -Solution: Utilized batch processing and database transactions to maintain consistency.<br>
 -Challenge: Filling missing timestamps for irregular data. <br>
 Solution: Used Pandas to resample data and interpolate missing values. <br>
 -Challenge:<br>
-Ensuring reusability and modularity. <br>
-Solution: Followed object-oriented design principles and modularized the codebase.<br>

Steps Taken:<br>

Dropped rows with missing sensor_value.<br>

Removed rows with invalid sensor_value (e.g., negative values for power_consumption).<br>

Dropped duplicate rows.<br>

b. SQL Queries Total Power Consumption Per Site: 
   SELECT site_id,
   SUM(sensor_value) AS total_power_consumption FROM Sensor_Data WHERE
   sensor_name = 'power_consumption' GROUP BY site_id,period,year;
Meters with Highest Power Usage Per Site: 
    SELECT site_id, meter_id,
    MAX(sensor_value) AS max_power FROM Sensor_Data WHERE sensor_name =
    'power_consumption' GROUP BY site_id, meter_id; 
Missing Timestamps:
   SELECT site_id, meter_id FROM Sensor_Data GROUP BY site_id, meter_id
   HAVING COUNT(DISTINCT timestamp)< (SELECT COUNT(DISTINCT timestamp)
    FROM Sensor_Data);
How to run
 - Execute the command "sqlite3 iot_db.db" in project directory to enter into sqllite3 shell.
-Run command .databases to create Database iot_db
- Run .exit to exit from sqlite3 shell.  -
-Install dependencies using requirements.txt file
- Run the python script from your project directory using the following command
- python main.py  - Metrics data are saved into iot_db database 
- Plots will be saved as \'.png\' files under subdirectory visualizations_biweekly
- CSV reports are generated in subdirectory reports
