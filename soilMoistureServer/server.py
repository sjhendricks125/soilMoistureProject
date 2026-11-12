from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "soil_data.csv" 
DATA_HEADER = ["timestamp", "raw_value", "saturation_percent"] 

def log_sensor_data(raw_value, saturation_percent, path=DATA_FILE):
    #Appends a sensor reading to the CSV file and creates the header if the file doesn't exist 
    file_exists = False #flag to check if file exists 
    try:
        with open(path, "r", newline=""): #try and open the file in read mode
            file_exists = True #marks that the file exists
    except FileNotFoundError:
        file_exists = False #file doesn't exist

    with open(path, "a", newline="") as f: #open file in append mode (a) 
        writer = csv.writer(f) #csv writer object: used to write rows to the CSV file
        if not file_exists:
            writer.writerow(DATA_HEADER) #writes header as first line if file is brand new
        writer.writerow([ #append data to row with timestamp, raw value and saturation % 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), raw_value, f"{saturation_percent:04.1f}"])

def get_latest(path=DATA_FILE):
    try:
        with open(path, "r", newline="") as f: #open csv in read mode 
            reader = list(csv.reader(f)) #read all rows into a list
            if reader: 
                return reader[-1] #returns the latest row from the CSV file
    except FileNotFoundError:
        pass
    return None #returns None if file doesn't exist or is empty

def get_all(path=DATA_FILE):
    try:
        with open(path,"r", newline="") as f: #open file in read mode
            return list(csv.reader(f)) #read all rows into a list and returns it
    except FileNotFoundError:
        pass
    return [] #returns an empty list if file doesn't exist or is empty

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/log_sensor", methods=["GET"])
def log_sensor():
    raw_value = request.args.get("raw") #reads value of raw from the query parameters

    if raw_value is not None: #check if raw parameter is provided
        try:
            raw_num = float(raw_value) 
            saturation_percent = (470 - raw_num)/3 #convert raw value to a percentage 
            if saturation_percent > 100:
                saturation_percent = 100
            elif saturation_percent < 0:
                saturation_percent = 0
            log_sensor_data(raw_num, saturation_percent) #log the sensor data to the CSV file
            return f"<p>Data logged: Raw={raw_num}, Saturation={saturation_percent:04.1f}%</p>", 200 #confirmation msg
        except ValueError: #if raw val can't be converted to float
            return "<p>Invalid sensor reading received.</p>", 400 #error msg

    return "<p>Missing 'raw' parameter.</p>", 400 #error msg for missing raw parameter

@app.route("/history")
def history():
    rows = get_all() #retrieve all rows from csv
    headers = rows[0] if rows else DATA_HEADER #use first row as a header 
    readings = rows[1:] if rows else [] #use all rows except first for readings
    return render_template("history.html", headers=headers, readings=readings)

@app.route("/latest")
def latest():
    #write this later
    latest_row = get_latest()
    return render_template("latest.html", latest=latest_row)


    #flask --app  server run --host=IP --port=5000`


