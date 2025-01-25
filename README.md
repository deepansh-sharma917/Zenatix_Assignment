

**Created By: Deepansh Sharma** <br>
**Description :** It includes all the required steps to execute the  project assignment  <br>
**Creation Dt :**19-Jan-2025  <br>

**How to run** <br>
 -Install virtualenvironment libreary using pip in project directory and follow the following steps <br>
 - python -m venv venv <br>
 - venv\Scripts\activate     # Windows <br>
 - Execute the command "sqlite3 iot_db.db" in project directory to enter into sqllite3 shell. <br>
 -Run command .databases to create Database iot_db <br>
 -Run .exit to exit from sqlite3 shell.  - <br>
**Install dependencies using requirements.txt file <br>- Run the python script from your project directory using the following command** <br>
    **python main.py**  - Metrics data are saved into iot_db database <br> 
    **Plots will be saved as .png files under subdirectory visualizations_biweekly** <br>
    **CSV reports are generated in subdirectory reports** <br>
**To run the Dockerized Solution**<br>
  **Prerequisites**<br>
   -Docker should be installed<br>
   **Steps To Follow**<br>
   -Open command shell and type **docker build -t iot_sensor-app .**<br>
   -Then to run a container **docker run -it --rm iot_sensor-app**<br>
