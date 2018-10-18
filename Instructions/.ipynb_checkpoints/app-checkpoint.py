#
# FLASK app for generating Weather data to consumable JSON-ified API
#

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create an engine to a SQLite database file called `hawaii.sqlite`
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of measurement date and prcp information from the last year """
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()
    
    # Create a dictionary from the row data and append to a list
    precipitation_values = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_values.append(prcp_dict)
        
        # Jasonify the list
        
        return jasonify(precipitation_values)


@app.route("/api/v1.0/stations")
def stations():
        """ List of stations from the Dataset"""
    stati = session.query(Measurement.station).all()
    
        stationslist = [stati]
        
        return jasonify(stationslist)
    

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs for the previous year"""
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-01-01", Measurement.date <= "2017-01-01").all()
    
    
     # Create a dictionary from the row data and append to a list
    temp_obs = []
    for o in tob_results:
        tob_dict = {}
        tob_dict["date"] = o.date
        tob_dict["tobs"] = o.tobs
        temp_obs.append(tob_dict)
        
        # Jasonify the list
        
        return jasonify(tob_dict)
    
    
@app.route("/api/v1.0/<start>")
def temps_start(start):
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    temperatures_start = list(np.ravel(results))

    return jsonify(temperatures_start)



@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)


if __name__ == "__main__":
    app.run(debug=True)
