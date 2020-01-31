import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
session = Session(engine)


Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Step 2 - Climate App
# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Use FLASK to create your routes.

app = Flask(__name__)

# Home page.
# List all routes that are available.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

# /api/v1.0/precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():

# Date of latest data point in the database = 2017-08-23

# Calculate the date 1 year ago from the last data point in the database

    Year_Ago = dt.date(2017, 8, 23)- dt.timedelta(days=365)    

    """Return a list of the precipitation data"""
    # Query all precipitation data from last 12 months
    Query_for_last_12_months_precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= Year_Ago).all()

    session.close()

    Query_for_last_12_months_precipitation_data = list(np.ravel(Query_for_last_12_months_precipitation_data))

    return jsonify(Query_for_last_12_months_precipitation_data)

    # Create a dictionary from the row data and append to a list of all_precipitation_data
    # all_precipitation_data = []
    # for date, prcp in Query_for_last_12_months_precipitation_data:
    #     precipitation_data_dict = {}
    #     precipitation_data_dict["date"] = date
    #     precipitation_data_dict["prcp"] = prcp
    #     all_precipitation_data.append(precipitation_data_dict)

    # return jsonify(all_precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)


    """Return a list of the station data"""
    Station_Data = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    session.close()

    return jsonify(Station_Data)

    # # Create a dictionary from the row data and append to a list of all_station_data
    # all_station_data = []
    # for station, count in Station_Data:
    #     station_data_dict = {}
    #     station_data_dict["station"] = station
    #     station_data_dict["count"] = count
    #     all_station_data.append(station_data_dict)

    # return jsonify(all_station_data)

@app.route("/api/v1.0/tobs")
def tobs():

    """Return a list of the tobs data"""
    # Query all tobs data from last 12 months
    
    Year_Ago = dt.date(2017, 8, 23)- dt.timedelta(days=365)  
    
    Query_for_last_12_months_precipitation_data_for_station_with_most_observations = session.query(Measurement.tobs, func.count(Measurement.tobs)).\
    group_by(Measurement.tobs).\
    filter(Measurement.date > Year_Ago).\
    filter(Measurement.station == 'USC00519281').all()

    Query_for_last_12_months_precipitation_data_for_station_with_most_observations

    Query_for_last_12_months_precipitation_data_for_station_with_most_observations = list(np.ravel(Query_for_last_12_months_precipitation_data_for_station_with_most_observations))

    return jsonify(Query_for_last_12_months_precipitation_data_for_station_with_most_observations)

    # # Create a dictionary from the tobs data and append to a list of tobs_data
    # tobs_data = []
    # for tobs, count in tobs_data:
    #     tobs_data_dict = {}
    #     tobs_data_dict["tobs"] = tobs
    #     tobs_data_dict["count"] = count
    #     tobs_data.append(tobs_data_dict)

    # return jsonify(tobs_data)

if __name__ == '__main__':
    app.run(debug=True)