package frsf.tibus.prediction.model;

import frsf.tibus.prediction.model.averagespeed.Route;

public class Bus {
	
	protected Route route;
	protected Integer id;
	protected Float lat, lon;
	
	public Bus(Integer id, Route route) {
		super();
		this.route = route;
		this.id = id;
	}
	
	public Integer getId() {
		return id;
	}
	public void setId(Integer id) {
		this.id = id;
	}
	public Float getLat() {
		return lat;
	}
	public void setLat(Float lat) {
		this.lat = lat;
	}
	public Float getLon() {
		return lon;
	}
	public void setLon(Float lon) {
		this.lon = lon;
	}

	public String getRouteName() {
		return this.route.getRouteName();
	}
}
