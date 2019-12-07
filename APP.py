from flask import Flask, jsonify
import sqlalchemy
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'Home' page!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    oneyear_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).order_by(Measurement.date).all()
    session.close()
    
    oneyear_data_d = []
    for date, prcp in oneyear_data:
        data_dict = {}
        data_dict["date"] = date
        data_dict["prcp"] = prcp
        oneyear_data_d.append(data_dict)
    return jsonify(oneyear_data_d)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    list_of_stations = session.query(Measurement.station.distinct()).all()
    session.close()
    
    return jsonify(list_of_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    oneyear_tempdata = session.query(Measurement.date,Measurement.tobs).\
               filter(Measurement.date > year_ago).all()
    session.close()
    
    oneyear_tempdata_d = []
    for date, tobs in oneyear_tempdata:
        tdata_dict = {}
        tdata_dict["date"] = date
        tdata_dict["tobs"] = tobs
        oneyear_tempdata_d.append(tdata_dict)
    return jsonify(oneyear_tempdata_d)

@app.route("/api/v1.0/<start>")
def cals_temp(start):
    session = Session(engine)
    
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).all()
    
    session.close()
    
    tempdata = []
    for x in data:
        tdict = {}
        tdict["Tmin"] = x[0]
        tdict["Tavg"] = x[1]
        tdict["Tmax"] = x[2]
        tempdata.append(tdict)
    
    return jsonify(tempdata)
    
@app.route("/api/v1.0/<start>/<end>")
def cal_temp(start,end):
    session = Session(engine)
    
    data1 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    
    tempdata1 = []
    for x in data1:
        tdict1 = {}
        tdict1["Tmin"] = x[0]
        tdict1["Tavg"] = x[1]
        tdict1["Tmax"] = x[2]
        tempdata1.append(tdict1)
    
    return jsonify(tempdata1)

    
if __name__ == "__main__":
    app.run(debug=True)