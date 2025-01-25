import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Create Tables in SQLite Database
def create_tables():
    try:

        # Connect to SQLite database (it will create the database file if it doesn't exist)
        conn = sqlite3.connect("iot_db.db")
        cursor = conn.cursor()

        # Create table site 
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sites (
            site_id VARCHAR(100) PRIMARY KEY,
            site_name VARCHAR(100)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Meters (
            meter_id VARCHAR(100) PRIMARY KEY,
            site_id VARCHAR(100),
            FOREIGN KEY (site_id) REFERENCES sites (site_id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sensor_Data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_id VARCHAR(100),
            meter_id VARCHAR(100),
            timestamp VARCHAR(100),
            sensor_name VARCHAR(100),
            sensor_value FLOAT(10,2),
            status VARCHAR(100),
            year int(10),
            month int(10),
            week_no int(10),
            period int(10),
            FOREIGN KEY (site_id) REFERENCES sites (site_id),
            FOREIGN KEY (meter_id) REFERENCES meters (meter_id)
        )
        ''')
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Period_Metrics (
            site_id TEXT,
            period INTEGER,
            year INTEGER,
            average_consumption FLOAT(10,2),
            max_consumption FLOAT(10,2),
            total_consumption FLOAT(10,2),
            FOREIGN KEY (site_id) REFERENCES sites (site_id)
        )
        """)



      


        


        conn.commit()
        print("Tables created successfully!")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        conn.close()

# 2. DataLoader Class: Load and Clean Data
class DataLoader:
    def __init__(self, csv_file, db_file):
        self.csv_file = csv_file
        self.db_file = db_file
    def load_data(self):
        """
        Load data from the provided CSV file into a pandas DataFrame.
        """
        try:
            data = pd.read_csv(self.csv_file)
            print("Data loaded successfully from CSV.")
            return data
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None

    def clean_data(self, data):
        """
        Clean the data by handling missing or invalid sensor values.
        """
        data = data.dropna()  # Drop rows with missing values
        data = data[data['sensor_value'] >= 0]  # Filter out invalid sensor values (negative values)
        return data



    def load_to_db(self, data):
        """
        Load cleaned data into the database.
        """
        try:
            conn = sqlite3.connect(self.db_file)
            data.to_sql('Sensor_Data', conn, if_exists='append', index=False)
            cursor = conn.cursor()
            cursor.execute("""
        UPDATE Sensor_Data
        SET year = strftime('%Y', timestamp),
            month = strftime('%m', timestamp),
            week_no=strftime('%W', timestamp),
            period=strftime('%W', timestamp)/2
        """)
            conn.commit()
            print("Cleaned data loaded into database.")
        except sqlite3.Error as e:
            print(f"Error loading data to DB: {e}")
        finally:
            conn.close()

# 3. DatabaseHandler Class: Execute SQL Queries
class DatabaseHandler:
    def __init__(self, db_file):
        self.db_file = db_file

    def execute_query(self, query, params=None):
        """
        Executes a query (e.g., SELECT, INSERT, UPDATE) in the database.
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                conn.commit()

        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
        finally:
            conn.close()

# 4. SQL Queries to be Executed
def get_total_power_consumption():
    query = """
    SELECT site_id, SUM(sensor_value) AS total_power_consumption
    FROM Sensor_Data
    WHERE sensor_name = 'power_consumption'
    GROUP BY site_id,period,year;
    """
    return query

def get_highest_power_usage_meters():
    query = """
    SELECT site_id, meter_id, MAX(sensor_value) AS max_power
    FROM Sensor_Data
    WHERE sensor_name = 'power_consumption'
    GROUP BY site_id, meter_id;
    """
    return query

def get_missing_timestamps():
    query = """
    SELECT site_id, meter_id
    FROM Sensor_Data
    GROUP BY site_id, meter_id
    HAVING COUNT(DISTINCT timestamp) < (SELECT COUNT(DISTINCT timestamp) FROM Sensor_Data);
    """
    return query

# 5. DataPreProcessor Class: Process Data with Pandas
class DataPreProcessor:
    def __init__(self, db_file):
        self.db_file = db_file

    def fetch_data_from_db(self):
        query = "SELECT * FROM Sensor_Data"
        db_handler = DatabaseHandler(self.db_file)
        data = db_handler.execute_query(query)
        return pd.DataFrame(data, columns=['id', 'site_id', 'meter_id', 'timestamp', 'sensor_name', 'sensor_value', 'status'])

    def normalize_data(self, data):
        """
        Normalize the sensor values (e.g., scale power values between 0 and 1).
        """
        data['sensor_value'] = (data['sensor_value'] - data['sensor_value'].min()) / (data['sensor_value'].max() - data['sensor_value'].min())
        return data

    def create_timeseries(self, data):
        """
        Create a time-series DataFrame with timestamps as the index.
        """
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.set_index('timestamp', inplace=True)
        return data

    def fill_missing_timestamps(self, data):
        """
        Fill missing timestamps with interpolated values.
        """
        data = data.resample('5T').interpolate(method='linear')
        return data

# 6. MetricsCalculator Class: Calculate Metrics
class MetricsCalculator:
    def __init__(self, db_file):
        self.db_file = db_file


    def calculate_metrics_period(self):
        query = """
        SELECT site_id,period,year, AVG(sensor_value) AS average_consumption, MAX(sensor_value) AS max_consumption, SUM(sensor_value) AS total_consumption
        FROM Sensor_Data
        WHERE sensor_name = 'power_consumption'
        GROUP BY site_id,year,period;
        """
        db_handler = DatabaseHandler(self.db_file)
        metrics_data = db_handler.execute_query(query)

        # Store metrics in the metrics table
        for metric in metrics_data:
            insert_query = """
            INSERT OR REPLACE INTO Period_Metrics (site_id,period,year,average_consumption, max_consumption, total_consumption)
            VALUES (?, ?, ?, ?,?,?);
            """
            db_handler.execute_query(insert_query, metric)

# 7. GraphGenerator Class: Generate Plots
class GraphGenerator:
    def __init__(self, db_file):
        self.db_file = db_file
    # Create a dictionary to store data for each site
    def generate_plots_period(self):
            query = """
                SELECT 
                    site_id, period,
                    AVG(average_consumption) AS avg_consumption,
                    MAX(max_consumption) AS max_consumption,
                    SUM(total_consumption) AS total_consumption
                FROM Period_Metrics
                GROUP BY site_id, year, period
            """
            db_handler = DatabaseHandler(self.db_file)
            metrics_data = db_handler.execute_query(query)
            if not metrics_data:
                print("No data found in the metrics table. Ensure metrics are calculated before generating plots.")
                return

            # Extract data
            sites = sorted(list(set(row[0] for row in metrics_data)))
            periods = sorted(list(set(row[1] for row in metrics_data)))

            # Create a dictionary to store data for each site
            site_data = {site: {"avg": [], "max": [], "total": []} for site in sites}
            for row in metrics_data:
                site_id, period, avg, max_, total = row
                site_data[site_id]["avg"].append(avg)
                site_data[site_id]["max"].append(max_)
                site_data[site_id]["total"].append(total)

            # Metrics for plotting
            metrics = {
                "Average Period Consumption": ("avg", "visualizations_biweekly/average_period_consumption.png", "Average Period-BiWeekly Consumption"),
                "Maximum Period Consumption": ("max", "visualizations_biweekly/max_period_consumption.png", "Maximum Period-BiWeekly Consumption"),
                "Total Period Consumption": ("total", "visualizations_biweekly/total_period_consumption.png", "Total Period-Biweekly Consumption"),
            }

            # Plot settings
            x = np.arange(len(periods))  # x positions for months
            width = 0.2  # Width of bars

            for metric_name, (key, filename, title) in metrics.items():
                fig, ax = plt.subplots()
                for i, site in enumerate(sites):
                    # Create bars for each site
                    site_values = site_data[site][key]
                    bar_positions = x + (i - len(sites) / 2) * width
                    bars = ax.bar(bar_positions, site_values, width, label=f"{site}")

                    # Add values on top of bars
                    for bar in bars:
                        yval = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha="center", va="bottom")

                # Set labels and title
                ax.set_xlabel("Period")
                ax.set_ylabel("Values")
                ax.set_title(title)
                ax.set_xticks(x)
                ax.set_xticklabels(periods)
                ax.legend()

                # Save plot as an image file
                plt.tight_layout()
                plt.savefig(filename)
                plt.close(fig)

            print("Plots have been successfully generated and saved.")
        




# 8. DataReportGenerator Class: Generate CSV Reports
class DataReportGenerator:
    def __init__(self, db_file):
        self.db_file = db_file

    def generate_reports_period(self):
        query = "SELECT * FROM Period_Metrics"
        db_handler = DatabaseHandler(self.db_file)
        metrics_data = db_handler.execute_query(query)

        # Save the metrics data to CSV
        df = pd.DataFrame(metrics_data, columns=['site_id','period','year','average_consumption', 'max_consumption', 'total_consumption'])
        df.to_csv('reports/metrics_report_period.csv', index=False)
        print("Metrics report saved as metrics_report_period.csv")




# Main Execution
if __name__ == "__main__":
    # Step 1: Create tables in the database
    create_tables()

    # Step 2: Load and clean data
    data_loader = DataLoader("IoT_Sensor_Data.csv", "iot_db.db")
    data = data_loader.load_data()
    cleaned_data = data_loader.clean_data(data)
    data_loader.load_to_db(cleaned_data)

    # Step 3: Calculate metrics
    metrics_calculator = MetricsCalculator("iot_db.db")
    metrics_calculator.calculate_metrics_period()




    # Step 4: Generate Graphs
    graph_generator = GraphGenerator("iot_db.db")
    graph_generator.generate_plots_period()

    # # Step 5: Generate Data Report
    report_generator = DataReportGenerator("iot_db.db")
    report_generator.generate_reports_period()
    



