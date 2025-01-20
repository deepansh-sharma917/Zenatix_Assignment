

Created By: Deepansh Sharma__
Description : It includes all the required steps to execute the  project assignment 
Creation Dt :19-Jan-2025 

Step 1: Database Design Database Schema: Use a database  SQLite  to store the data. You need tables for storing sensor
readings, metadata (e.g., site and meter info), and any processed
metrics. 
CREATE TABLE Sites ( site_id VARCHAR(100) PRIMARY KEY,
site_name VARCHAR(100) ); 
CREATE TABLE Meters ( meter_id TEXT PRIMARY
KEY, site_id TEXT, FOREIGN KEY (site_id) REFERENCES sites(site_id) );
CREATE TABLE Sensor_Data ( id INTEGER PRIMARY KEY AUTOINCREMENT, site_id
VARCHAR(100), meter_id VARCHAR(100), timestamp VARCHAR(100), sensor_name
VARCHAR(100), sensor_value FLOAT(10,2), status TEXT, year int(10), month
int(10), week_no int(10), period int(10), FOREIGN KEY (site_id)
REFERENCES sites (site_id), FOREIGN KEY (meter_id) REFERENCES meters
(meter_id) ); 
CREATE TABLE Period_Metrics ( site_id TEXT, period
INTEGER, year INTEGER, average_consumption FLOAT(10,2), max_consumption
FLOAT(10,2), total_consumption FLOAT(10,2), FOREIGN KEY (site_id)
REFERENCES sites (site_id) ); 
Modular Object Oriented Solution 
a. Class Descriptions 
1.DataLoader -Loads data from the provided CSV file.
 -Cleans and preprocesses the data: -Handles missing or inconsistent
  data. -Flags and filters out invalid sensor values (e.g., negative
  values for temperature or power consumption). -Removes duplicate rows
  and missing columns. -Loads the cleaned data into the database.
2.DatabaseHandler: 
   -Manages database connection and execution of
    queries. 
    -Loads cleaned data into the database. 
3.DataPreProcessor:
   Fetches data from the database. 
    -Processes data using Pandas and NumPy:
    -Normalizes sensor values (e.g., scales power consumption values between
0 and 1). 
    -Creates a time-series DataFrame with timestamps as the index.
    -Fills missing timestamps using interpolation. 4.MetricsCalculator:
    -Calculates metrics such as averages, maximums, and daily sums. -Stores
     metrics in the database for visualization.
5.GraphGenerator: -Generates
   plots/visualizations from the metrics data: 
      -Average consumption.
     -Maximum consumption.
     -Total power consumption. 
     -Saves plots as PNG files. 
6.DataReportGenerator: 
-Exports calculated metrics into a CSV
report for stakeholders. 
Challenges and Solutions 
 -Challenge: Handling large datasets and ensuring data integrity. 
 -Solution: Utilized batch processing and database transactions to maintain consistency.
 -Challenge: Filling missing timestamps for irregular data. 
 Solution: Used Pandas to resample data and interpolate missing values.
 -Challenge:
-Ensuring reusability and modularity. 
-Solution: Followed object-oriented design principles and modularized the codebase.

Steps Taken:

Dropped rows with missing sensor_value.

Removed rows with invalid sensor_value (e.g., negative values for
power_consumption).

Dropped duplicate rows.

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
