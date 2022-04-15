import numpy as np
import datetime as dt
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from sqlalchemy import or_


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    #List all available api routes.
    return (
        f"Available Routes:<br/>"
        f"Total precipitation 12 months before the most recent records: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Tobs of the most active station 12 months before the most recent records: /api/v1.0/tobs<br/>"
        f"TMIN, TAVG, and TMAX for all dates greater than and equal to the given start date(YYYY-MM-DD): /api/v1.0/<start><br/>"
        f"TMIN, TAVG, and TMAX for all dates greater than and equal to the given start and end date(YYYY-MM-DD/YYYY-MM-DD):/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.
       session = Session(bind=engine)
       precipitation = session.query(Measurement.date, func.sum(Measurement.prcp)).\
       filter(func.strftime(Measurement.date)>=(datetime.datetime.strptime(\
       session.query(func.max(Measurement.date))[0][0],"%Y-%m-%d")- relativedelta(years=1))).\
       group_by(Measurement.date).order_by(Measurement.date).all()
        
       session.close()

       prcp_dict = {}
       prcp_list = []
       for date, prcp in precipitation:
           prcp_dict={date:prcp}
           prcp_list.append(prcp_dict)
       return jsonify(prcp_list)
            

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.

    session = Session(bind=engine)
    sel = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    stations = session.query(*sel).all()

    session.close()
    station_list = []
    for station,name,latitude,latitude,elevation in stations:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = latitude
        station_dict["Elevation"] = elevation
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    # Return a JSON list of temperature observations (TOBS) for the previous year.
    
    session = Session(bind=engine)
    
    most_recent_date = session.query(func.max(Measurement.date)).all()
    end_date=datetime.datetime.strptime(most_recent_date[0][0],"%Y-%m-%d")
    before_12_months = end_date - relativedelta(years=1)
    most_active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    temperature_most_active = session.query(Measurement.date, Measurement.tobs).\
    filter(func.strftime(Measurement.date) >= before_12_months).\
    filter(Measurement.station== most_active_stations[0]).all()

    session.close()
    tob_list = [tob[1] for tob in temperature_most_active]

    return jsonify(tob_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    
    session = Session(bind=engine)

    canonicalized=datetime.datetime.strptime(start,"%Y-%m-%d")-datetime.timedelta(days=1)
    
    lowest_tobs = session.query(Measurement.date,func.min(Measurement.tobs)).\
        filter(func.strftime(Measurement.date) >= canonicalized).all()
    highest_tobs = session.query(Measurement.date,func.max(Measurement.tobs)).\
        filter(func.strftime(Measurement.date) >= canonicalized).all()
    avg_tobs = session.query(Measurement.date,func.avg(Measurement.tobs)).\
        filter(func.strftime(Measurement.date) >= canonicalized).all()
    
    session.close()
    
    tob_list=[
        {"Lowest Tobs":lowest_tobs[0][1]},
        {"Highest Tobs":highest_tobs[0][1]},
        {"Average Tobs":avg_tobs[0][1]}
    ]
    return jsonify(tob_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

    session = Session(bind=engine)

    canonicalized_start=datetime.datetime.strptime(start,"%Y-%m-%d")-datetime.timedelta(days=1)
    canonicalized_end=datetime.datetime.strptime(end,"%Y-%m-%d")

    lowest_tobs = session.query(Measurement.date,func.min(Measurement.tobs)).\
        filter(func.strftime(Measurement.date) >= canonicalized_start).\
        filter(func.strftime(Measurement.date) <= canonicalized_end).all()
    highest_tobs = session.query(Measurement.date,func.max(Measurement.tobs)).\
        filter(func.strftime(Measurement.date) >= canonicalized_start).\
        filter(func.strftime(Measurement.date) <= canonicalized_end).all()
    avg_tobs = session.query(Measurement.date,func.avg(Measurement.tobs)).\
        filter(func.strftime(Measurement.date) >= canonicalized_start).\
        filter(func.strftime(Measurement.date) <= canonicalized_end).all()
    
    session.close()
    
    tob_list=[
        {"Lowest Tobs":lowest_tobs[0][1]},
        {"Highest Tobs":highest_tobs[0][1]},
        {"Average Tobs":avg_tobs[0][1]}
    ]
    return jsonify(tob_list)



if __name__ == "__main__":
    app.run(debug=True)