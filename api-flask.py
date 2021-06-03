# stephen.peters@gmail.com
# SQLalchemy Challenge homework
# Data Analytics Bootcamp, spring 2021

# let's make an API with Flask
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

# create engine to hawaii.sqlite
#engine = create_engine("sqlite:///Resouces/hawaii.sqlite")
# refuses to read the file unless it's in the same dir, for some reason
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#print(' -- let\'s look at some of our data from Measurement')
measurement_df = pd.read_sql_query("select date, prcp, station from measurement where (date like '2017%')\
                                  or (date like '2016-09%')\
                                  or (date like '2016-10%')\
                                  or (date like '2016-11%')\
                                  or (date like '2016-12%')", engine)
measurements_flask = measurement_df[['date', 'prcp']].copy()

print('Hello Friendly User!')
#print('our measurements dataframe is...')
measurements_flask.dropna(axis = 0, how = 'any', inplace=True)
measurements_flask.set_index('date', inplace=True)
#print(measurements_flask.head())
measurements_data = measurements_flask.to_dict()

#print('Now getting our TOBS data for one year from station USC00519281')
tobs_df = measurement_df[measurement_df.station != "USC00519281" ]

#print('our TOBS dataframe is...')
tobs_df.dropna(axis = 0, how = 'any', inplace=True)
tobs_data = tobs_df[['date', 'prcp']].copy()
tobs_data.set_index('date', inplace=True)
tobs_flask = tobs_data.to_dict()
#print(tobs_data.head())

temps_df = pd.read_sql_query("select date, tobs from measurement", engine)
#print(temps_df)

# import station data
stations_df = pd.read_sql_query("SELECT * FROM station", engine)
#print(stations_df)
stations_data = stations_df.to_dict()

# setup our Flask app
app = Flask(__name__)

# create index route
@app.route("/")
def home():
  print("server received request for 'home' page...")
  return (
      f"<blockquote>"
      f"<h2>Welcome to Hawaii Weather API home page</h2><br/>"
      f"<b>Available Routes:</b><br/>"
      f"<ul>"
      f"<li><a href='/api/v1.0/precipitation' target='_blank'>/api/v1.0/precipitation</a>  <br> -- Returns date and precipitation observation for every record in our data."

      f"<li><a href='/api/v1.0/stations' target='_blank'>/api/v1.0/stations</a> <br> -- Returns all the data about our observation stations"
      
      f"<li><a href='/api/v1.0/tobs' target='_blank'>/api/v1.0/tobs</a>"
      f"<br> -- Returns the dates and temperature observations of the most active station for the last twelve months of data."
      
      f"<li>/api/v1.0/&ltstart date&gt"
      f"<br> -- Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date through the last date on record."
      f"<br> -- Date format needs to be YYYY-MM-DD."
      
      f"<li>/api/v1.0/&ltstart date&gt/&ltend date&gt"      
      f"<br> -- Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date through the end date."
      f"<br> -- Date format needs to be YYYY-MM-DD."     
       
      f"<li>/human-readable/&ltstart date&gt"
      f"<br> -- same thing as above, only  formatted for reading by humans"
      
      f"<li>/human-readable/&ltstart date&gt/&ltend date&gt"
      f"<br> -- same thing as above, only formatted for reading by humans"      
      f"</ol>"
      f"</blockquote>"
    )
    
@app.route("/api/v1.0/precipitation")
def measurements():
    """Return the measurement data as json"""
    print("server received request for precipitation data...")
    return jsonify(measurements_data)     
    
@app.route("/api/v1.0/stations")
def stations():
    """Return the stations data as json"""
    print("server received request for stations data...")
    return jsonify(stations_data)    

@app.route("/api/v1.0/<start_date>")
def zeetemps(start_date):
    """here we get our aggregate stats for our date range"""
    print("server received request for tobs stats start to end of data...")
    # correct for dates before the start of our data
    if start_date < '2010-01-01':
      start_date = '2010-01-01'
    # set end date
    end_date = '2017-08-23'
    range_df = temps_df[(temps_df['date'] >= start_date) & (temps_df['date'] <= end_date)]
    lowest = range_df['tobs'].min()
    highest = range_df['tobs'].max()
    average = range_df['tobs'].mean()
    output = {'TMIN': lowest, 'TMAX': highest, 'TAVG': average}
    return jsonify(output)
    
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    """here we get our aggregate stats for our date range"""
    print("server received request for tobs stats start date to end date...")
    # correct for dates before the start of our data
    if start_date < '2010-01-01':
      start_date = '2010-01-01'
    # correct for dates beyond the end of our data
    if end_date > '2017-08-23':
      end_date = '2017-08-23'
    range_df = temps_df[(temps_df['date'] >= start_date) & (temps_df['date'] <= end_date)]
    lowest = range_df['tobs'].min()
    highest = range_df['tobs'].max()
    average = range_df['tobs'].mean()
    output = {'TMIN': lowest, 'TMAX': highest, 'TAVG': average}
    return jsonify(output)    

@app.route("/human-readable/<start_date>")
def temps(start_date):
    """here we get our aggregate stats for our date range"""
    print("server received request for human readable tobs stats start date to end date...")
    # correct for dates before the start of our data
    if start_date < '2010-01-01':
      start_date = '2010-01-01'
    # set end date
    end_date = '2017-08-23'
    range_df = temps_df[(temps_df['date'] >= start_date) & (temps_df['date'] <= end_date)]
    lowest = range_df['tobs'].min()
    highest = range_df['tobs'].max()
    average = range_df['tobs'].mean()
    observations = range_df['tobs'].count()
    output = {'TMIN': lowest, 'TMAX': highest, 'TAVG': average}
    return (
      f"<blockquote><br><br>"
      f"<h2>Thanks for checking the weather in Hawaii!</h2><br/>"
      f"You asked for a <i>start date</i> of: <b>{start_date}</b><br>"
      f"...and an <i>end date</i> of: <b>{end_date}</b><br><br>"
      f"There are <b>{observations}</b> observation records in this date range.<br><br>"
      f"The maximum observed temperature in that date range is: <b>{highest}</b><br>"
      f"The minimum observed temperature in that date range is: <b>{lowest}</b><br>"
      f"The average temperature in that date range is: <b>{round(average, 4)}</b><br>"
      f"</blockquote>"
      )
    
@app.route("/human-readable/<start_date>/<end_date>")
def human_start_end(start_date, end_date):
    """here we get our aggregate stats for our date range"""
    print("server received request for human readable tobs stats start date to end date...")
    # correct for dates before the start of our data
    if start_date < '2010-01-01':
      start_date = '2010-01-01'
    # correct for dates beyond the end of our data
    if end_date > '2017-08-23':
      end_date = '2017-08-23'
    range_df = temps_df[(temps_df['date'] >= start_date) & (temps_df['date'] <= end_date)]
    lowest = range_df['tobs'].min()
    highest = range_df['tobs'].max()
    average = range_df['tobs'].mean()
    observations = range_df['tobs'].count()
    return (
      f"<blockquote><br><br>"
      f"<h2>Thanks for checking the weather in Hawaii!</h2><br/>"
      f"You asked for a <i>start date</i> of: <b>{start_date}</b><br>"
      f"...and an <i>end date</i> of: <b>{end_date}</b><br><br>"
      f"There are <b>{observations}</b> observation records in this date range.<br><br>"      
      f"The maximum observed temperature in that date range is: <b>{highest}</b><br>"
      f"The minimum observed temperature in that date range is: <b>{lowest}</b><br>"
      f"The average temperature in that date range is: <b>{round(average, 4)}</b><br>"
      f"</blockquote>"
      )

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the TOBS data of station USC00519281 from the last 12 months as json"""
    print("server received request for the last year of TOBS data...")
    return jsonify(tobs_flask)    
  
if __name__ == "__main__":
  app.run(debug=True)  
  
  