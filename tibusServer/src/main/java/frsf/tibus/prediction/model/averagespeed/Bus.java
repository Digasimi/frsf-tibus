package frsf.tibus.prediction.model.averagespeed;

import frsf.tibus.domain.BusPositionData;

public class Bus {
	
	Route route;
	Integer id;
	Float lat, lon;
	Stop currentStop;
	
	public Bus(Integer id, Route route) {
		super();
		this.route = route;
		this.id = id;
		this.currentStop = null;
	}
	
	public Stop getCurrentStop() {
		return currentStop;
	}
	public void setCurrentStop(Stop currentStop) {
		this.currentStop = currentStop;
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

	public void processPosition(BusPositionData busPosition) 
	{
		if(currentStop == null)
		{
			Stop nearestStop = route.findNearestStop(busPosition, currentStop);
			
			if(nearestStop != null)
				currentStop = nearestStop;
		}		
	}
}
