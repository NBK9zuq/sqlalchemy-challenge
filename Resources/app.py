# 1. import dependencies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime

from flask import Flask, jsonify

#2.  Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# reflect the tables
inspector = inspect(engine)
inspector.get_table_names()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# 3. Create an app
app = Flask(__name__)


# 4. Create Routes

#A. HOME ROUTE:  Home page, listing all routes available
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
 	f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
	f"/api/v1.0/tobs<br/>"
	f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


#B.  PRECIPITATION ROUTE
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")

def precipitation():
	session = Session(engine)
	results = session.query(Measurement.date, Measurement.prcp).all()
	session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
	for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation(precipitation_dict)

    return jsonify(all_precipitation)


#B.  STATION ROUTE
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")

def stations():
	session = Session(engine)
	results = session.query(Station.station).all()
	session.close()

Station_list = list(np.ravel(results))
return jsonify(Station_list)


#C.  TOBS ROUTE
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")

def TOBS():
	session = Session(engine)
	
	temp_12mo = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= 2016-08-23).filter(Measurement.station == USC00519281).order_by(Measurement.date).all()
	session.close()

Station_list = list(np.ravel(temp_12mo))
return jsonify(Station_list)


#D. START ROUTE
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")

#Calculate the tobs stats for the date that matches the path variable supplied by the user, or a 404 if not

def tempstats_greaterthan_startdate(start):
	session = Session(engine)
	format = "%m/%d/%Y"
	cleaned_date = datetime.datetime.strftime(start, format)
	results = session.query(Measurement.date, func.min(Measurement.tobs), func.average(Measurement.tobs), func.min(Measurement.tobs)).\
		group_by(Measurement.date).filter(Measurement.date >= cleaned_date).all()

	session.close()

tobs_list = list(np.ravel(results))
return jsonify(tobs_list)

#E. END ROUTE
#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")

def tempstats_greaterthan_startdate(start_date, end_date):
	session = Session(engine)
	format = "%m/%d/%Y"
	cleaned_start = datetime.datetime.strptime(start_date, format)
	cleaned_end = datetime.datetime.strptime(end_date, format)
	results1 = session.query(Measurement.date, func.min(Measurement.tobs), func.average(Measurement.tobs), func.min(Measurement.tobs)).\
		group_by(Measurement.date).filter(Measurement.date > cleaned_date).all()

	session.close()

tobs1_list = list(np.ravel(results1))
return jsonify(tobs1_list)

#5.  Run from the main Python prompt
if __name__ == "__main__":
    app.run(debug=True)
