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

print(' -- let\'s look at some of our data from Measurement')
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

print('Now getting our TOBS data for one year from station USC00519281')
tobs_df = measurement_df[measurement_df.station != "USC00519281" ]


#print('our TOBS dataframe is...')
tobs_df.dropna(axis = 0, how = 'any', inplace=True)
tobs_data = tobs_df[['date', 'prcp']].copy()
tobs_data.set_index('date', inplace=True)
tobs_flask = tobs_data.to_dict()
#print(tobs_data.head())

# import station data
# test importing the station csv
stations_df = pd.read_csv('Resources/station_data.csv')
stations_df = stations_df.drop(columns = ['id', 'Unnamed: 0'])
stations_data = stations_df.to_dict()


# setup our Flask app
app = Flask(__name__)

# create index route
@app.route("/")
def home():
  print("server received request for 'home' page...")
  return (
      f"<blockquote>"
      f"Welcome to Flask API home page, kind visitor<br/>"
      f"<b>Available Routes:</b><br/>"
      f"<ul>"
      f"<li><a href='/api/v1.0/precipitation' target='_blank'>/api/v1.0/precipitation</a>  <br> -- Return the JSON representation of your dictionary."
      f"<br> -- Convert the query results to a dictionary using `date` as the key and `prcp` as the value.  <b>DONE!</b>"
      f"<li><a href='/api/v1.0/stations' target='_blank'>/api/v1.0/stations</a> <br> -- Return a JSON list of stations from the dataset. <b>DONE!</b>"
      f"<li><a href='/api/v1.0/tobs' target='_blank'>/api/v1.0/tobs</a>"
      f"<br> -- Query the dates and temperature observations of the most active station for the last year of data."
      f"<br> -- Return a JSON list of temperature observations (TOBS) for the previous year.   <b>DONE!</b>"
      f"<li><a href='/api/v1.0/test' target='_blank'>testing url</a>"     
      f"<li>/api/v1.0/&ltstart&gt and /api/v1.0/&ltstart&gt/&ltend&gt"
      f"<br> -- Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."
      f"<br> -- When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."
      f"<br> -- When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."
      f"<li><a href='/api/v1.0/justice-league/real_name/ target='_blank'>/api/v1.0/justice-league/real_name/</a> add real name and get back super name <b>DONE REMOVE!</B>"
      f"</ol>"
      f"</blockquote>"
    )
    
@app.route("/api/v1.0/precipitation")
def measurements():
    """Return the measurement data as json"""

    return jsonify(measurements_data)     
    
@app.route("/api/v1.0/stations")
def stations():
    """Return the stations data as json"""

    return jsonify(stations_data)    

@app.route("/api/v1.0/test/<foo_var>/<foo2_var>")
def test(foo_var, foo2_var):
    """let us just test picking up those variables"""
    insult = "nixnut"
    print("server received request for about page...")
    return (
      f"Welcome to the test page, you {insult}.<br/>"
      f"you typed... {foo_var}<br>"
      f"...and you also typed... {foo2_var}<br>"
      f"and your mother wears combat boots."
      )

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the TOBS data of station USC00519281 from the last 12 months as json"""

    return jsonify(tobs_flask)    
    
@app.route("/api/v1.0/justice-league/real_name/<real_name>")
def justice_league_by_real_name(real_name):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = real_name.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["real_name"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"sorry": f"Character with real_name {real_name} not found."}), 404    
  
@app.route("/about")  
def about():
  insult = "nixnut"
  print("server received request for about page...")
  return (
    f"Welcome to ABOUT page, you {insult}.<br/>"
    f"and your mother wears combat boots."
    )
  
if __name__ == "__main__":
  app.run(debug=True)  
  
  