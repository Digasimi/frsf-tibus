package frsf.tibus.prediction.model.averagespeed;

public class Bus {
	Route route;
	Integer id;
	Float lat, lon;
	Stop currentStop;
	
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
}
