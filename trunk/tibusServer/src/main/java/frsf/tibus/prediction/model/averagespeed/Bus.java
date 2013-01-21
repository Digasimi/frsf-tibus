package frsf.tibus.prediction.model.averagespeed;

import org.joda.time.Period;

import com.bbn.openmap.proj.Length;

import frsf.tibus.domain.BusPositionData;

public class Bus {
	
	private Route route;
	private Integer id;
	private Float lat, lon;
	
	// Parada asignada según posición recibida
	private Stop currentStop;
	private Stop previousStop;
	
	// Ubicación real
	private BusPositionData previousLocation;
	private BusPositionData currentLocation;
	
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

	protected void processPosition(BusPositionData busPosition) 
	{
		Stop nearestStop;
		if(currentStop == null)
			nearestStop = route.findNearestStop(busPosition);
		else
			nearestStop = route.findNearestStop(busPosition, currentStop);
		
//		if(nearestStop != null)
		
		previousStop = currentStop;
		currentStop = nearestStop;
		
		previousLocation = currentLocation;
		currentLocation = busPosition;
		
		this.lat = busPosition.getLat();
		this.lon = busPosition.getLon();
	}

	public Double calculateAverageSpeed() {
		
		if(previousLocation != null && currentLocation != null)
		{
			Double distance = Length.METER.fromRadians(previousLocation.getCoordinates().distance(currentLocation.getCoordinates()));
			Integer timeDifference = new Period(previousLocation.getDate(), currentLocation.getDate())
											.toStandardSeconds()
											.getSeconds();
			
			return distance / timeDifference;
		}
		else
			return null;
	}

	public String getRouteName() {
		return this.route.getRouteName();
	}

	public Stop getPreviousStop() {
		return this.previousStop;
	}

	public BusPositionData getCurrentLocation() {
		return this.currentLocation;
	}
}
